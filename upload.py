from ftplib import FTP
from os import environ
from pathlib import Path
import sys, json, curses


JAVA_SINC = environ['JAVA_SINC_DIR']
USUARIO=enciron['USUARIO_FTP']
SENHA=environ['SENHA_FTP']

def verificaArquivos():
    projetos = {
        'ord': {},
        'troppus':{},
        'seg': {},
    }

    for projeto in projetos:
        arquivo = Path(JAVA_SINC +'/'+ projeto + '/war/target/' +projeto+'.war')
        if arquivo.is_file():
            projetos[projeto]['exist'] = True
            projetos[projeto]['path'] = arquivo
    return {k: v for k, v in projetos.items() if v['exist'] == True}

def carregarPreferencias():
    try:
        with open('pref.ini', 'w') as prefs:
            return json.load(prefs)
    except:
        return {}

def salvarPreferencias(prefs):
    with open('pref.ini', 'w') as _file:
        json.dump(prefs, _file)

def start():
    #pref = carregarPreferencias()
    if not JAVA_SINC:
        print('Variável de ambiente JAVA_SINC_DIR não definida')
    else:
        ftp = FTP('ftp.supportweb.com.br')
        try:
            ftp.login(USUARIO, SENHA)
            diretorio = input('Digite o diretório de upload: ')
            ftp.cwd(diretorio)
            #if not pref[diretorio]:
                #pref[diretorio] = {}
            for nome, arquivo in verificaArquivos().items():
                confirma = input(f'Deseja fazer upload de {nome}.war? (s/n)')

                if confirma.upper() == 'S':
                    #pref[diretorio][nome] = True
                    try:
                        file = open(str(arquivo['path']), 'rb')
                        ftp.storbinary(f"stor {nome}.war", file)
                        file.close()
                    except:
                        print("Erro inesperado ao abrir arquivo: ",
                              + sys.exc_info()[0])
            ftp.quit()
            #salvarPreferencias()
        except:
            print("Falha ao conectar-se ao servidor")
            print("Erro inesperado: ", sys.exc_info()[0])

if __name__ == "__main__":
    start()
