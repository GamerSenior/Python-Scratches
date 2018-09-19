import urwid, ftp

def exit_program(button):
    raise urwid.ExitMainLoop()

def connect():
    return None

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
        'callback': upload,
    },{
        'label': 'Upload Relatórios',
        'callback': uploadRelatorio
    }
       , 'Sair']

def menu_buttom(caption, callback):
    button = urwid.Button(caption)
    urwid.connect_signal(button, 'click', callback)
    return urwid.AttrMap(button, None, focus_map='reversed')

def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    for item in menu_abertura:
        body.append(menu_buttom(item['label'], item['callback']))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

main = urwid.Padding(menu('Support Uploader BETA 0.1', menu_abertura), left=2, right=2)
top = urwid.Overlay(main, urwid.SolidFill('\N{MEDIUM SHADE}'),
                    align='center', width=('relative', 60),
                    valign='middle', height=('relative', 60),
                    min_width=20, min_height=9)
urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
