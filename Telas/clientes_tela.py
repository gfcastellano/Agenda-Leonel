from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout



class Clientes_tela(Screen):
    
    def on_pre_enter(self):
        print('Entrando em Mapa_tela')
        app = MDApp.get_running_app()
        self.dados_clientes = app.dados_clientes
        children = MDApp.get_running_app().root.get_screen('Clientes_tela').ids.box_scroll.children
        print('CHILDREN:',len(children))
        if len(children) < 1:
            self.adicionar_clientes()

    def adicionar_clientes(self):
        print('Adicionando clientes na tela')
        scroll = MDApp.get_running_app().root.get_screen('Clientes_tela').ids.box_scroll
        for cliente in self.dados_clientes:
            #print(cliente)
            scroll.add_widget(Cliente(codigo = str(cliente['codigo']),nome_fantasia = cliente['nome_fantasia']))


class Cliente(BoxLayout):
    def __init__(self, codigo='', nome_fantasia='',**kwargs):
        super().__init__(**kwargs)
        self.ids.codigo.text = codigo
        self.ids.nome_fantasia.text = nome_fantasia

