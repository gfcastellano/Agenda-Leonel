from kivy.uix.screenmanager import Screen


class Menu(Screen):
    def on_pre_enter(self):
        print('Entrando em Menu_tela')