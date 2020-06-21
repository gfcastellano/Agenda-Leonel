import kivy
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from Telas.menu_tela import Menu
from Telas.mapa_tela import Mapa_tela
from Mapa.mapa import Mapa
from Telas.clientes_tela import Clientes_tela
from Telas.busca_tela import Busca_tela
from kivy.uix.popup import Popup
from Popups.popups import Popup_LeituraDados
from Telas.info_tela import Info_tela
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from Telas.adicionar_cliente_tela import Adicionar_cliente_tela


import json


class Gerenciador(ScreenManager):
    pass


class MainApp(MDApp):
    dados_clientes =[]
    popup_leituradados = None
    telas = ['Menu_tela']
    
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        return Gerenciador()

    def on_start(self):
        self.carregar_clientes()
        clientes_tela = Clientes_tela()
        clientes_tela.adicionar_clientes(self.dados_clientes)
        self.popup_leituradados = Popup_LeituraDados()

    def carregar_clientes(self):
        with open('clientes.json', 'r') as file:
            try:
                self.dados_clientes = json.load(file)
                print('clientes.json carregado com sucesso,' 'tamanho:',len(self.dados_clientes))
            except FileNotFoundError:
                print('clientes.json não achado no diretório')
    
MainApp().run()
