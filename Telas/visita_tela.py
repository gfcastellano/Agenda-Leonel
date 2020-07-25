from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window


class Visita_tela(Screen):
    def on_pre_enter(self):
        print('Entrando em Visita_tela')
        app = MDApp.get_running_app()
        app.registrar_tela()
        Window.bind(on_keyboard=app.voltar)
        
        self.dados_clientes = app.dados_clientes
        self.dados_visitas  = app.dados_visitas