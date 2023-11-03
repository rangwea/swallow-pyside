# -*- coding: utf-8 -*-
import shutil
import sqlite3
import time
import json
import logging
import webbrowser
from pathlib import Path
from subprocess import Popen
from zipfile import ZipFile

import psutil
import tomli
import tomli_w
from git import repo, GitCommandError, Repo
from psutil import NoSuchProcess

from swallow.cossync import COS
from swallow.exceptions import BizException
from swallow.models import Article, Menu

SITE_NAME = 'site'
CONF_FILE = 'conf.json'
DB_NAME = 'db'

site_static_path = Path()
site_images_path = Path()  # type Path

get_site_image_url_prefix = '/get_site_image/'

init_sql = '''
CREATE TABLE t_article(
    aid BIGINT PRIMARY KEY,
    title VARCHAR NOT NULL,
    tags VARCHAR,
    categories VARCHAR,
    create_time DATETIME,
    update_time DATETIME
);
CREATE INDEX idx_t_article_title ON t_article(title);
CREATE INDEX idx_t_article_tags ON t_article(tags);
CREATE INDEX idx_t_article_categories ON t_article(categories);
CREATE INDEX idx_t_article_create_time ON t_article(create_time);
CREATE INDEX idx_t_article_update_time ON t_article(update_time);
'''


def use_logging(func):
    def wrapper(*args):
        try:
            r = func(*args)
            logging.info(f'call {func.__name__}({args}), return: {r}')
            return r
        except BizException as be:
            raise be
        except Exception as e:
            logging.error(f'sever error:{e}', exc_info=True)

    return wrapper


def sqlite_dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def read_matter(article_path: Path):
    matter = ''
    with article_path.open(encoding='utf-8') as f:
        i = 0
        for line in f.readlines():
            if i > 1:
                break
            if line.startswith('+++'):
                i = i + 1
            else:
                matter = matter + line
    return tomli.loads(matter)


class Hugos:
    def __init__(self, base_dir: Path, app_home_path: Path, site_name):
        logging.info(f'init hugos:{self}')
        self.hugo = str((base_dir / 'lib' / 'hugo').absolute())
        self.app_home_path = app_home_path
        self.site_name = site_name
        self.site_path = app_home_path / site_name
        self.articles_path = self.site_path / 'content' / 'post'
        self.pre_pid_path = self.site_path / 'pre.pid'
        self.public_path = self.site_path / 'public'
        self.static_img_path = self.site_path / 'static' / 'images'
        self.static_cname_path = self.site_path / 'static' / 'CNAME'
        self.images_path = self.articles_path
        self.themes_path = self.site_path / 'themes'
        self.images_base_url = '/images/'
        self.site_conf_path = self.site_path / 'config.toml'
        self.site_about_path = self.site_path / 'content' / 'about' / 'index.md'
        self.themes_zip_path = base_dir / 'lib' / 'themes.zip'
        self.lib_conf_path = base_dir / 'lib' / 'config.toml'

    def new_site(self):
        if self.site_path.exists():
            logging.info(f'Not will be new site, because site has be existed:{self.site_path}')
            return
        Popen([self.hugo, 'new', 'site', self.site_name], cwd=self.app_home_path).wait()
        self.articles_path.mkdir(parents=True, exist_ok=True)
        self.site_about_path.parent.mkdir(exist_ok=True)
        self.site_about_path.touch(exist_ok=True)
        self.static_img_path.mkdir(exist_ok=True)
        self.static_cname_path.touch(exist_ok=True)

        if self.site_conf_path.exits():
            self.site_conf_path.unlink()
        shutil.copyfile(self.lib_conf_path, self.site_conf_path)

        with ZipFile(self.themes_zip_path) as z:
            z.extractall(path=self.themes_path)

        logging.info(f'new a site: {self.site_name}')

    def preview(self):
        if self.pre_pid_path.exists():
            e_pid = self.pre_pid_path.read_text()
            if e_pid:
                try:
                    p = psutil.Process(int(e_pid))
                    if 'hugo' in p.name() and p.is_running():
                        return
                    else:
                        self.pre_pid_path.write_text('')
                except NoSuchProcess:
                    pass

        pid = Popen([self.hugo, 'server'], cwd=self.site_path).pid
        self.pre_pid_path.write_text(str(pid))
        logging.info('start preview')

    def close_pre(self):
        pid = self.pre_pid_path.read_text()
        if pid:
            try:
                psutil.Process(int(pid)).kill()
            except NoSuchProcess:
                pass
        self.pre_pid_path.write_text('')

    def generate(self):
        Popen([self.hugo], cwd=self.site_path).wait()
        logging.info('hugo generate')

    def article_path(self, aid):
        return self.articles_path / str(f'{aid}') / 'index.md'

    def loads_site_conf(self):
        with self.site_conf_path.open('rb') as f:
            return tomli.load(f)


class Conf:
    def __init__(self, app_home_path):
        self.conf_path = app_home_path / CONF_FILE  # type: Path
        if not self.conf_path.exists():
            self.conf_path.write_text('{}')

    def get(self, key):
        with self.conf_path.open() as f:
            return json.load(f).get(key)

    def save(self, key, content):
        with self.conf_path.open('r') as f:
            conf = json.load(f)
            conf[key] = content
        with self.conf_path.open('w') as f:
            json.dump(conf, f, indent=4, ensure_ascii=False)
            logging.info(f'save conf:{key}={conf}')


class DB:
    def __init__(self, db_path: Path):
        self.db_path = db_path

        if not self.db_path.exists():
            conn = self._conn()
            cur = conn.cursor()
            cur.executescript(init_sql)
            conn.commit()
            cur.close()
            conn.close()

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def fetchall(self, sql):
        with self._conn() as conn:
            conn.row_factory = sqlite_dict_factory
            cur = conn.execute(sql)
            d = cur.fetchall()
            cur.close()
            return d

    def fetchone(self, sql):
        with self._conn() as conn:
            conn.row_factory = sqlite_dict_factory
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchone()

    def save(self, table, m: dict):
        placeholders = ', '.join(['?'] * len(m))
        columns = ', '.join(m.keys())
        sql = f"INSERT OR REPLACE INTO {table} ({columns}) VALUES ({placeholders})"
        conn = self._conn()
        cur = conn.cursor()
        cur.execute(sql, list(m.values()))
        conn.commit()

    def execute(self, sql):
        conn = self._conn()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()


def get_msg(e:GitCommandError):
    s = e.stderr.replace("stderr: 'fatal: ", '')
    s = s.strip("'")
    return s


def git_create_remote(git_type, c, work_path):
    repository = c.get('repository')
    token = c.get('token')
    url = repository.replace('https://', f'https://{token}@')
    try:
        r = repo.Repo.init(work_path)
        r.delete_remote(git_type)
        r.create_remote(git_type, url)
        r.remote(git_type).fetch()
    except GitCommandError as e:
        raise BizException(get_msg(e))


def git_push(git_type, work_path):
    try:
        r = repo.Repo.init(work_path)
        r.index.add(['*'])
        r.index.commit(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')
        r.remote(git_type).push(refspec=f'main:main').raise_if_error()
    except GitCommandError as e:
        raise BizException(get_msg(e))


class Api:
    def __init__(self, base_dir, app_home_path):
        self.base_dir = base_dir
        self.hugos = Hugos(base_dir, app_home_path, SITE_NAME)
        self.conf = Conf(app_home_path)
        self.app_home_path = app_home_path
        self.db = DB(app_home_path / DB_NAME)

        # new a site
        self.hugos.new_site()
        self.window = None
        self.repo = Repo.init(self.hugos.public_path)  # type: Repo

    @use_logging
    def site_preview(self):
        self.hugos.preview()
        webbrowser.open('http://localhost:1313/', new=1, autoraise=True)

    @use_logging
    def site_deploy(self):
        # exec hugo to generate public
        self.hugos.generate()
        # sync public to cos
        if self.conf.get('cos') and self.conf.get('cos').get('appid'):
            cos = COS(**self.conf.get('cos'), root=str(self.hugos.public_path.absolute()))
            cos.sync()
        if self.conf.get('gitee'):
            git_push('gitee', self.hugos.public_path)
        if self.conf.get('github'):
            git_push('github', self.hugos.public_path)

    @use_logging
    def conf_get(self, key):
        return self.conf.get(key)

    @use_logging
    def conf_save(self, key, content):
        cname = content.get('cname')
        if cname:
            self.hugos.static_cname_path.write_text(cname.strip())

        if key == 'gitee' or key == 'github':
            old_conf = self.conf.get(key)
            if old_conf.get('repository') != content.get('repository') or old_conf.get('token') != content.get('token'):
                git_create_remote(key, content, self.hugos.public_path)

        return self.conf.save(key, content)

    @use_logging
    def article_list(self, search=None):
        sql = 'select * from t_article'
        if search:
            sql += f" where title like '%{search}%' or tags like '%{search}%' or categories like '%{search}%'"
        sql += ' order by create_time desc'
        return [Article(**a) for a in self.db.fetchall(sql)]

    def article_save(self, aid, article):
        if aid == 'about':
            article_path = self.hugos.site_about_path
            article_path.write_text(article)
        else:
            article_path = self.hugos.article_path(aid)
            article_dir = article_path.parent
            if not article_dir.exists():
                article_dir.mkdir()

            # replace front matter and write file
            with article_path.open('w+', encoding='utf-8') as f:
                i = 0
                for line in article.splitlines():
                    if (i == 0 or i == 1) and line.startswith('```'):
                        f.write(line.replace('```', '+++\n'))
                        i = i + 1
                    else:
                        f.write(line + '\n')

            matter = read_matter(article_path)
            d = {
                'aid': aid,
                'title': matter.get('title'),
                'create_time': matter.get('date'),
                'update_time': time.strftime('%Y-%m-%d, %H:%M:%S', time.localtime()),
                'tags': ','.join(matter.get('tags')),
                'categories': ','.join(matter.get('categories')),
            }
            self.db.save('t_article', d)

    @use_logging
    def article_get(self, aid):
        article = ''
        if aid == 'about':
            article_path = self.hugos.site_about_path
        else:
            article_path = self.hugos.article_path(aid)

        with article_path.open(encoding='utf-8') as f:
            i = 0
            for line in f.readlines():
                if (i == 0 or i == 1) and line.startswith('+++'):
                    line = line.replace('+++', '```')
                    i = i + 1
                    article = article + line
                else:
                    article = article + line

        return article

    @use_logging
    def article_del(self, aid):
        self.db.execute(f'delete from t_article where aid={aid}')
        self.hugos.article_path(aid).unlink(missing_ok=True)
        if aid:
            shutil.rmtree(site_images_path / str(aid), ignore_errors=True)

    @use_logging
    def site_conf_get(self):
        site_config = self.hugos.loads_site_conf()
        keys = ('title', 'description', 'theme', 'copyright', 'author')
        return {i: site_config.get(i) for i in keys}

    @use_logging
    def site_conf_save(self, new_site_conf):
        site_config = self.hugos.loads_site_conf()
        site_config.update(new_site_conf)
        with self.hugos.site_conf_path.open('wb') as f:
            tomli_w.dump(site_config, f)

    @use_logging
    def get_menu_conf(self):
        site_conf = self.hugos.loads_site_conf()
        return [Menu(**a) for a in site_conf.get('menu').get('main')]
