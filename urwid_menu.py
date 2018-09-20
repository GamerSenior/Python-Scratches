import urwid, sys, logging
from ftplib import FTP
from os import environ
from pathlib import Path
from pudb import set_trace

logger = logging.getLogger('urwid-log')

ftp = FTP('ftp.supportweb.com.br')

def exit_program(button):
    raise urwid.ExitMainLoop()

class MenuPrincipal(urwid.Filler):
    def __init__(self):
        self.projetos_upload = []
        upload_projetos = urwid.Button('Upload Projeto')
        upload_relatorios = urwid.Button('Upload Relatórios')
        exit = urwid.Button('Sair')
        urwid.connect_signal(upload_projetos, 'click', self.upload_projetos)
        urwid.connect_signal(exit, 'click', exit_program)
        pile = []
        pile.append(upload_projetos)
        pile.append(upload_relatorios)
        pile.append(exit)
        super().__init__(urwid.Pile(pile))

    def troca_diretorio(self, widget):
        diretorio = self.diretorio.get_edit_text()
        try:
            ftp.cwd(diretorio)
        except:
            logger.error('Erro ao trocar de diretório', sys.exc_info()[0])

    def escolher_diretorio(self, widget):
        self.diretorio = urwid.Edit('Diretório', '')
        errors = urwid.Text('')
        entrar = urwid.Button('Entrar no diretório')
        urwid.connect_signal(entrar, 'click', self.troca_diretorio)
        pile = urwid.Pile([diretorio, errors, entrar])
        main.original_widget = urwid.Filler(pile)

    def upload_projetos(self, widget):
        projetos = []
        ord = urwid.CheckBox('ORD', user_data='ord')
        seg = urwid.CheckBox('SEG', user_data='seg')
        troppus = urwid.CheckBox('TROPPUS', user_data='troppus')
        div = urwid.Divider()
        upload = urwid.Button('Realizar Upload')
        sair = urwid.Button('Voltar')
        urwid.connect_signal(sair, 'click', self.voltar)
        projetos.append(ord)
        projetos.append(seg)
        projetos.append(troppus)
        for projeto in projetos:
                urwid.connect_signal(projeto, 'change',
                                 lambda s, p: self.projetos_upload.append(p)
                                 if s else self.projetos_upload.remove(p))
        projetos.append(div)
        projetos.append(upload)
        projetos.append(sair)
        main.original_widget = urwid.Filler(urwid.Pile(projetos))

    def upload_relatorios(self, widget):
        return None

    def voltar(self, widget):
        main.original_widget = self;

class LoginBox(urwid.Filler):
    def __init__(self):
        self.useredit = urwid.Edit('Usuario: ', '')
        self.senhaedit = urwid.Edit('Senha: ', '', mask='*')
        self.erros = urwid.Text('')
        self.loginbtn = urwid.Button('Login')
        self.exitbtn = urwid.Button('Sair')
        urwid.connect_signal(self.loginbtn, 'click', self.login)
        urwid.connect_signal(self.exitbtn, 'click', exit_program)
        div = urwid.Divider()
        pile = urwid.Pile([self.useredit, self.senhaedit, div, self.erros,
                       urwid.AttrMap(self.loginbtn, None, focus_map='reversed'),
                       urwid.AttrMap(self.exitbtn, None, focus_map='reversed')
                       ])
        super().__init__(pile)

    def login(self, widget):
        username = self.useredit.get_edit_text()
        password = self.senhaedit.get_edit_text()
        try:
            ftp.login(username, password)
            main.original_widget = MenuPrincipal();
        except:
            logger.info('Deu ruim!', sys.exc_info()[0])
            self.erros.set_text('Usuario ou senha inválidos')

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
