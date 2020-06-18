from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRaisedButton

class Popup_LeituraDados(MDDialog):
    title = 'AGUARDE'
    text = 'Acessando base de dados, isso pode levar alguns segundos ...'

    def __init__(self):
        super().__init__()
        self.size_hint = [.6,.4]

class Popup_Maps(MDDialog):
    title= 'Deseja ir para rotas do Maps?'
    #buttons = MDRaisedButton(text='SIM')

    def __init__(self):
        super().__init__()
        self.size_hint = [0.9,0.9]
        self.events_callback = MDApp.get_running_app().root.get_screen('Info_tela').abrir_maps
