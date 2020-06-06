from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from menu import Menu
from mapa_tela import Mapa_tela
from mapa import Mapa

import json


class Gerenciador(ScreenManager):
    pass


class MainApp(MDApp):
    dados_clientes =[]
    def build(self):
        return Gerenciador()

    def on_start(self):
        self.carregar_clientes()

    def carregar_clientes(self):
        with open('clientes.json', 'r') as file:
            try:
                self.dados_clientes = json.load(file)
                print('clientes.json carregado com sucesso,' 'tamanho:',len(self.dados_clientes))
            except FileNotFoundError:
                print('clientes.json não achado no diretório')

MainApp().run()