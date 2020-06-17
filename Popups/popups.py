from kivymd.uix.dialog import MDDialog

class Popup_LeituraDados(MDDialog):
    title = 'Isso pode levar alguns segundos... aguarde!'

    def __init__(self):
        super().__init__()
        self.size_hint = [.6,.4]