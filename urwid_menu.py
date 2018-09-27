import urwid, sys, logging
from ftplib import FTP
from os import environ
from pathlib import Path
from pudb import set_trace

logger = logging.getLogger('urwid-log')

try:
    ftp = FTP('ftp.supportweb.com.br')
    JAVA_SINC = environ['JAVA_SINC_DIR']
    RELATORIOS = environ['RELATORIOS_DIR']
except KeyError:
    logger.error('Falha ao buscar variáveis de ambiente')

def exit_program(button):
    raise urwid.ExitMainLoop()

class MenuPrincipal(urwid.Filler):
    def __init__(self):
        self.diretorio = urwid.Text('Diretório: ')
        div = urwid.Divider()
        upload_projetos = urwid.Button('Upload Projeto')
        upload_relatorios = urwid.Button('Upload Relatórios')
        exit = urwid.Button('Sair')
        urwid.connect_signal(upload_projetos, 'click', self.upload_projetos)
        urwid.connect_signal(exit, 'click', exit_program)
        pile = []
        pile.append(self.diretorio)
        pile.append(div)
        pile.append(upload_projetos)
        pile.append(upload_relatorios)
        pile.append(exit)
        super().__init__(urwid.Pile(pile))

    def upload_projetos(self, widget):
        main.original_widget = MenuUploadProjetos()

    def upload_relatorios(self, widget):
        return None

    def voltar(self, widget):
        main.original_widget = self;

class MenuUploadRelatorios(urwid.Filler):
    def __init__(self):
        self.relatorios = []

    def busca_relatorios(self, widget):
        path = Path(RELATORIOS)

class MenuUploadProjetos(urwid.Filler):
    def __init__(self):
        self.projetos = []
        self.mensagens = urwid.Text('')
        projetos = []
        ord = urwid.CheckBox('ORD', user_data='ord')
        seg = urwid.CheckBox('SEG', user_data='seg')
        troppus = urwid.CheckBox('TROPPUS', user_data='troppus')
        div = urwid.Divider()
        upload = urwid.Button('Realizar Upload')
        sair = urwid.Button('Voltar')
        urwid.connect_signal(upload, 'click', self.realiza_upload)
        urwid.connect_signal(sair, 'click', self.voltar)
        projetos.append(ord)
        projetos.append(seg)
        projetos.append(troppus)
        for projeto in projetos:
                urwid.connect_signal(projeto, 'change', self.escolhe_projetos)
        projetos.append(div)
        projetos.append(upload)
        projetos.append(sair)
        super().__init__(urwid.Pile([self.mensagens] + projetos))

    def voltar(self, widget):
        main.original_widget = MenuPrincipal()

    def escolhe_projetos(self, widget, escolha):
        set_trace()
        projeto = widget.get_label().lower()
        if(escolha):
            self.projetos.append(projeto)
        else:
            try:
                self.projetos.remove(projeto)
            except ValueError:
                pass

    def realiza_upload(self, widget):
        try:
            for projeto in self.projetos:
                arquivo = Path(f'{JAVA_SINC}/{projeto}/war/target/{projeto}.war')
                if arquivo.is_file():
                        file = open(str(arquivo), 'rb')
                        ftp.storbinary(f'stor {projeto}.war', file)
                        file.close()
            self.mensagens.set_text("Upload realizado com sucesso!")
        except:
            self.mensagens.set_text('Erro ao realizar upload')
            logger.error('Erro inesperado ao abrir arquivo: ',
                         sys.exc_info()[0])

class TelaDiretorio(urwid.Filler):
    def __init__(self):
        self.diretorio = urwid.Edit('Diretório: ', '')
        self.erros = urwid.Text('')
        entrar = urwid.Button('Entrar no diretório')
        urwid.connect_signal(entrar, 'click', self.troca_diretorio)
        pile = urwid.Pile([self.diretorio, self.erros, entrar])
        super().__init__(pile)

    def troca_diretorio(self, widget):
        diretorio = self.diretorio.get_edit_text()
        try:
            ftp.cwd(diretorio)
            main.original_widget = MenuPrincipal()
            main.original_widget.diretorio = diretorio
        except:
            self.erros.set_text('Erro ao acessar diretório')
            logger.error('Erro ao trocar de diretório', sys.exc_info()[0])

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
            main.original_widget = TelaDiretorio();
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
