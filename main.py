from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from menu import Menu
from mapa_tela import Mapa_tela
from mapa import Mapa


class Gerenciador(ScreenManager):
    pass


class MainApp(MDApp):
    def build(self):
        return Gerenciador()

MainApp().run()