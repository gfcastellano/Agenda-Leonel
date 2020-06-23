from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from voltar import Voltar
from Mapa.marcador import Marcador, Marcador_vermelho
from kivy.core.window import Window

class Mapa_tela(Screen):
    dados_clientes=[]
    lista_de_marcadores=[]
    
    def on_pre_enter(self):
        print('Entrando em Mapa_tela')
        app = MDApp.get_running_app()
        app.registrar_tela()
        Window.bind(on_keyboard=app.voltar)
        self.dados_clientes = app.dados_clientes
        children = self.ids.mapa.children
        if len(children) <= 2:
            self.adicionar_marcadores(self.dados_clientes)
        #for cliente in self.dados_clientes:
        #    if cliente['nome_fantasia'] not in self.lista_de_marcadores:
        #        self.adicionar_marcadores(cliente)
        

    def adicionar_marcadores(self,dados_cliente):
        print('Adicionando marcadores no Mapa')
        for cliente in self.dados_clientes:
            try:
                nome_fantasia, lat, lon = cliente['nome_fantasia'],cliente['lat'],cliente['lon']
                if nome_fantasia not in self.lista_de_marcadores:
                    self.ids.mapa.add_widget(Marcador(lat=lat,lon=lon)) #adiciona marcador
                    self.lista_de_marcadores.append(nome_fantasia) #adiciona nome a lista
            except:
                print('Não possivel adicionar marcador para o cliente:', nome_fantasia)
                continue
        
        print('Fim de adicionar_marcadores:',len(self.lista_de_marcadores))
        print('Ultimo cliente que foi adicionado marcador:', self.lista_de_marcadores[-1])
                

   
    
