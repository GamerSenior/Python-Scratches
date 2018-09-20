import urwid, sys, logging
from ftplib import FTP
from pudb import set_trace

logger = logging.getLogger('urwid-log')

#ftp = FTP('ftp.supportweb.com.br')
#username = ''
#password = ''

def exit_program(button):
    raise urwid.ExitMainLoop()

def log_in(edit):
    set_trace()
    try:
        print(username, password)
        ftp.login(username, password)
    except:
        print('Erro ao realizar login', sys.exc_info()[0])

def set_user(edit, content):
    logger.info(content)
    username = content

def set_pass(edit, content):
    logger.info(content)
    password = content

class LoginBox(urwid.Filler):
    def __init__(self):
        self.useredit = urwid.Edit('Usuario: ', '', align='center')
        self.senhaedit = urwid.Edit('Senha: ', '', mask='*', align='center')
        self.loginbtn = urwid.Button('Login')
        self.exitbtn = urwid.Button('Sair')
        urwid.connect_signal(self.loginbtn, 'click', self.login)
        urwid.connect_signal(self.exitbtn, 'click', exit_program)
        div = urwid.Divider()
        pile = urwid.Pile([self.useredit, self.senhaedit, div,
                       urwid.AttrMap(self.loginbtn, None, focus_map='reversed'),
                       urwid.AttrMap(self.exitbtn, None, focus_map='reversed')
                       ])
#        self.body = pile
        super().__init__(pile)

    def login(self, widget):
        username = self.useredit.get_edit_text()
        password = self.senhaedit.get_edit_text()
        set_trace()

def login_box():
    user = urwid.Edit('Usuario: ', '', align='center')
    urwid.connect_signal(user, 'change', set_user)
    passwd = urwid.Edit('Senha: ', '', mask='*', align='center')
    urwid.connect_signal(passwd, 'change', set_pass)
    login = urwid.Button('Login')
    urwid.connect_signal(login, 'click', log_in)
    exit = urwid.Button('Sair')
    urwid.connect_signal(exit, 'click', exit_program)
    div = urwid.Divider()
    pile = urwid.Pile([user, passwd, div,
                       urwid.AttrMap(login, None, focus_map='reversed'),
                       urwid.AttrMap(exit, None, focus_map='reversed')
                       ])

    return urwid.Filler(pile)

def connect(button):
    try:
        main.original_widget = LoginBox()
    except:
        print('Erro inesperado', sys.exc_info()[0])

menu_abertura = [
    {
        'label': 'Conectar FTP Support',
        'callback': connect,
    },{
        'label': 'Sair',
        'callback': exit_program,
    }
]

menu_principal = [
    {
        'label': 'Upload Projetos',
        'callback': None,
    },{
        'label': 'Upload Relatórios',
        'callback': None
    },{
        'label': 'Sair',
        'callback': exit_program,
    }
]

def menu_buttom(caption, callback):
    button = urwid.Button(caption)
    urwid.connect_signal(button, 'click', callback)
    return urwid.AttrMap(button, None, focus_map='reversed')

def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    for item in menu_abertura:
        body.append(menu_buttom(item['label'], item['callback']))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

main = urwid.Padding(menu('Support Uploader BETA 0.1', menu_abertura),
                     left=2, right=2)
top = urwid.Overlay(main, urwid.SolidFill('\N{MEDIUM SHADE}'),
                    align='center', width=('relative', 60),
                    valign='middle', height=('relative', 60),
                    min_width=20, min_height=9)
urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
