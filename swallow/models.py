class Article:

    def __init__(self, aid=None, title=None, tags=None, categories=None, create_time=None, update_time=None):
        self.aid = aid
        self.title = title
        self.tags = tags
        self.categories = categories
        self.create_time = create_time
        self.update_time = update_time


class Menu:

    def __init__(self, identifier=None, name=None, url=None, weight=None):
        self.identifier = identifier
        self.name = name
        self.url = url
        self.weight = weight