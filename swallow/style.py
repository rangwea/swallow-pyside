STYLE = '''
* {
    outline: 0px;
    color: #404040;
}
#mainWidget {
    background-color: #FFF;
}
#sidebar {
    background-color: rgb(236,236,236);
    min-width: 160px;
    max-width: 160px;
}
#logo {
    margin-top: 20px;
    margin-bottom: 5px;
}
#menu-item {
    font-size: 14px;
    border-style: none;
    padding: 10px;
    border-radius: 4px;
    margin-top: 8px;
    min-height: 18px;
    text-align: left; 
}
#menu-item:hover {
    background-color: rgb(220,220,220);
}
#menu-item:checked {
    background-color: rgb(109,162,235);
    color: #FFFFFF;
}
#sidebar_button {
    height: 24px;
    border: 1px solid #b7bdc8;
    border-radius: 12px;
}
#sidebar_button:hover {
    background-color: rgb(109,162,235);
    color: white;
}
#sidebar_button:disabled {
    background-color: rgb(220,220,220);
}
#article_list {
    background-color: white;
    border: none;
    margin: 15px;
}
#article_list::item {
    border: 1px solid rgb(230,230,230);
    height: 60px;
    border-radius: 7px;
    margin-bottom: 8px;
}
#article_list::item:hover {
    background-color: rgb(240,240,240);
}
#page_header {
    margin: 0px;
    max-height: 50px;
    min-height: 50px;
    border-bottom: 1px solid rgb(230,230,230);
}
#sidebar_right {
    margin: 0px;
    padding: 0px;
    outline:0px;
}
QTextEdit {
    background-color: #FFF;
    border: none;
    font-size: 14px;
    padding: 5px;
}
#conf_page::pane {
    background-color: #FFF;
    border: none;
}
#header-tab-btn {
    border: 1px solid rgb(220,220,220);
    font-size: 12px;
    padding: 5px;
    border-radius: 4px;
    width: 80px;
}
#header-tab-btn:hover {
    background-color: rgb(220,220,220);
}
#header-tab-btn:checked {
    background-color: rgb(109,162,235);
    color: #FFFFFF;
}
QLineEdit {
    border: 1px solid rgb(200, 200, 200);
    background-color: #FFF;
    max-width: 500px;
    min-width: 500px;
    height: 25px;
    padding: 0px;
    border-radius: 3px;
}
#icon_btn {
    min-width: 30px;
    max-width: 30px;
    min-height: 30px;
    max-height: 30px;
    border: none;
}
#delete_icon_btn {
    min-width: 100px;
    max-width: 100px;
    min-height: 30px;
    max-height: 30px;
    border: none;
}
#icon_btn:hover, #icon_btn:pressed, #delete_icon_btn:hover, #delete_icon_btn:pressed {
    background-color: rgb(225, 225, 225);
    border-radius: 15px;
}
#form_button {
    color: white;
    width: 70px;
    height: 30px;
    background: rgb(109, 162, 235);
    border-radius: 5px;
}
#form_button:hover {
    background-color: #1056da;
}
#QImage {
    width: 100px;
}
QMessageBox {
    background-color: white;
}
#edit {
    color: rgb(50,50,50)
}
QComboBox {
    border: 1px solid rgb(200, 200, 200);
    padding: 1px 18px 1px 3px;
    background-color: #FFF;
    min-width: 480px;
    max-width: 480px;
    height: 25px;
    border-radius: 3px;
}
QComboBox::drop-down {
    border: none;
}
QComboBox QAbstractItemView {
    outline: 0px solid gray;
    border: 1px solid rgb(200, 200, 200);
    selection-background-color: lightgreen; 
}
'''

PREVIEW_STYLE = '''
<style type="text/css">
html,body {overflow-x: hidden; overflow-y:auto}
th { background: rgb(200,200,200); }
img { width: 100%}
p { width: 100%; word-wrap:break-word; word-break:break-all; white-space: pre-line; }
blockquote { background: #f7f7f7; border-left: 6px solid #ccc; margin: 5px; padding: 5px; }
blockquote p { display: inline; font-size: 15px;}

pre {padding:2px}
td.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
span.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
td.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
span.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
.codehilite .hll { background-color: #ffffcc }
.codehilite { background: #f8f8f8; overflow-x:auto; margin-top:5px; margin-bottom:5px;}
.codehilite .c { color: #3D7B7B; font-style: italic } /* Comment */
.codehilite .err { border: 1px solid #FF0000 } /* Error */
.codehilite .k { color: #008000; font-weight: bold } /* Keyword */
.codehilite .o { color: #666666 } /* Operator */
.codehilite .ch { color: #3D7B7B; font-style: italic } /* Comment.Hashbang */
.codehilite .cm { color: #3D7B7B; font-style: italic } /* Comment.Multiline */
.codehilite .cp { color: #9C6500 } /* Comment.Preproc */
.codehilite .cpf { color: #3D7B7B; font-style: italic } /* Comment.PreprocFile */
.codehilite .c1 { color: #3D7B7B; font-style: italic } /* Comment.Single */
.codehilite .cs { color: #3D7B7B; font-style: italic } /* Comment.Special */
.codehilite .gd { color: #A00000 } /* Generic.Deleted */
.codehilite .ge { font-style: italic } /* Generic.Emph */
.codehilite .gr { color: #E40000 } /* Generic.Error */
.codehilite .gh { color: #000080; font-weight: bold } /* Generic.Heading */
.codehilite .gi { color: #008400 } /* Generic.Inserted */
.codehilite .go { color: #717171 } /* Generic.Output */
.codehilite .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.codehilite .gs { font-weight: bold } /* Generic.Strong */
.codehilite .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.codehilite .gt { color: #0044DD } /* Generic.Traceback */
.codehilite .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.codehilite .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.codehilite .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.codehilite .kp { color: #008000 } /* Keyword.Pseudo */
.codehilite .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.codehilite .kt { color: #B00040 } /* Keyword.Type */
.codehilite .m { color: #666666 } /* Literal.Number */
.codehilite .s { color: #BA2121 } /* Literal.String */
.codehilite .na { color: #687822 } /* Name.Attribute */
.codehilite .nb { color: #008000 } /* Name.Builtin */
.codehilite .nc { color: #0000FF; font-weight: bold } /* Name.Class */
.codehilite .no { color: #880000 } /* Name.Constant */
.codehilite .nd { color: #AA22FF } /* Name.Decorator */
.codehilite .ni { color: #717171; font-weight: bold } /* Name.Entity */
.codehilite .ne { color: #CB3F38; font-weight: bold } /* Name.Exception */
.codehilite .nf { color: #0000FF } /* Name.Function */
.codehilite .nl { color: #767600 } /* Name.Label */
.codehilite .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
.codehilite .nt { color: #008000; font-weight: bold } /* Name.Tag */
.codehilite .nv { color: #19177C } /* Name.Variable */
.codehilite .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
.codehilite .w { color: #bbbbbb } /* Text.Whitespace */
.codehilite .mb { color: #666666 } /* Literal.Number.Bin */
.codehilite .mf { color: #666666 } /* Literal.Number.Float */
.codehilite .mh { color: #666666 } /* Literal.Number.Hex */
.codehilite .mi { color: #666666 } /* Literal.Number.Integer */
.codehilite .mo { color: #666666 } /* Literal.Number.Oct */
.codehilite .sa { color: #BA2121 } /* Literal.String.Affix */
.codehilite .sb { color: #BA2121 } /* Literal.String.Backtick */
.codehilite .sc { color: #BA2121 } /* Literal.String.Char */
.codehilite .dl { color: #BA2121 } /* Literal.String.Delimiter */
.codehilite .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.codehilite .s2 { color: #BA2121 } /* Literal.String.Double */
.codehilite .se { color: #AA5D1F; font-weight: bold } /* Literal.String.Escape */
.codehilite .sh { color: #BA2121 } /* Literal.String.Heredoc */
.codehilite .si { color: #A45A77; font-weight: bold } /* Literal.String.Interpol */
.codehilite .sx { color: #008000 } /* Literal.String.Other */
.codehilite .sr { color: #A45A77 } /* Literal.String.Regex */
.codehilite .s1 { color: #BA2121 } /* Literal.String.Single */
.codehilite .ss { color: #19177C } /* Literal.String.Symbol */
.codehilite .bp { color: #008000 } /* Name.Builtin.Pseudo */
.codehilite .fm { color: #0000FF } /* Name.Function.Magic */
.codehilite .vc { color: #19177C } /* Name.Variable.Class */
.codehilite .vg { color: #19177C } /* Name.Variable.Global */
.codehilite .vi { color: #19177C } /* Name.Variable.Instance */
.codehilite .vm { color: #19177C } /* Name.Variable.Magic */
.codehilite .il { color: #666666 } /* Literal.Number.Integer.Long */
</style>
'''
