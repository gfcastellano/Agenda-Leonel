from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from Mapa.marcador import Marcador

class Mapa_tela(Screen):
    def on_pre_enter(self):
        print('Entrando em Mapa_tela')
        app = MDApp.get_running_app()
        self.dados_clientes = app.dados_clientes
        children = self.ids.mapa.children
        if len(children) <= 2:
            self.adicionar_marcadores()
        

    def adicionar_marcadores(self):
        print('Adicionando marcadores no Mapa')
        for cliente in self.dados_clientes:
            lat, lon = cliente['lat'],cliente['lon']
            try:
                self.ids.mapa.add_widget(Marcador(lat=lat,lon=lon))
            except:
                continue