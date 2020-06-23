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
from Telas.editar_tela import Editar_tela


import json


class Gerenciador(ScreenManager):
    pass


class MainApp(MDApp):
    dados_clientes =[]
    popup_leituradados = None
    telas = ['Menu_tela']
    data = {
        'point-of-sale': 'Vendas',
        'briefcase': 'Visitas'}
    
    
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

    def registrar_tela(self):
        try:        
            app = MDApp.get_running_app()
            app.telas.append(str(app.root.current_screen)[14:-2])
        except AttributeError: #para que no build não dê problemas
            pass

    def voltar(self,window,key,*args):
        if key ==27: #27 = esc
            app = MDApp.get_running_app()
            try:         
                tela_atual = str(app.telas[-1])
            except IndexError:
                app.telas = ['Menu_tela']
                tela_atual = str(app.telas[-1])
            try:
                ultima_tela = str(app.telas[-2])
            except IndexError:
                ultima_tela = tela_atual
            print('=========================')
            print('TELA_ATUAL: ', tela_atual)
            print('ULTIMA_TELA:', ultima_tela)
            print('TELAS:      ', app.telas)

            if ultima_tela == 'Info_tela' and tela_atual == 'Mapa_tela':
                app.root.transition.direction = 'left'                
                app.root.current = ultima_tela
            elif ultima_tela == 'Editar_tela' and tela_atual == 'Info_tela':
                app.root.transition.direction = 'right'                
                app.root.current = str(app.telas[-4])
                app.telas = app.telas[:-4]
            elif tela_atual == 'Menu_tela':
                app.root.transition.direction = 'left'                
                app.root.current = ultima_tela
            else:
                app.root.transition.direction = 'left'
                app.root.current = ultima_tela
                app.root.transition.direction = 'right'
            # Aqui faz com que o voltar não fique sempre pulando entre as duas ultimas telas
            if len(app.telas) > 2:
                try:  
                    if ultima_tela == app.telas[-3]:
                        app.telas = app.telas[:-2]
                except IndexError:
                    app.telas = app.telas[:-1]
            if len(app.telas) == 0:
                app.telas = ['Menu_tela']
            print('FINAL DE VOLTAR', app.telas)
            print('+++++++++++++++++++++++++++')
        if key == 113: # 113 = q
            app = MDApp.get_running_app()
            print(app.telas)

        return True

    def voltar_toolbar(self):
        app = MDApp.get_running_app()
        app.root.transition.direction = 'left'
        app.root.current = str(app.telas[-2])
        app.root.transition.direction = 'right'
        try:
            if app.telas[-1] == app.telas[-3]:
                app.telas = app.telas[:-2]
        except IndexError:
            app.telas = app.telas[:-1]
           
    
MainApp().run()
