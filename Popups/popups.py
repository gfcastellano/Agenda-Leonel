from kivymd.uix.dialog import MDDialog

class Popup_LeituraDados(MDDialog):
    title = 'AGUARDE!'
    text = 'Acessando base de dados, isso pode demorar...'

    def __init__(self):
        super().__init__()
        self.size_hint = [.6,.4]