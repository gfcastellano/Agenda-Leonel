from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from Mapa.marcador import Marcador
from kivy.core.window import Window

class Mapa_tela(Screen):
    def on_pre_enter(self):
        app = MDApp.get_running_app()
        gerenciador = app.root
        app.telas.append(str(gerenciador.current_screen)[14:-2])
        Window.bind(on_keyboard=self.voltar)
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

    def voltar(self,window,key,*args):
        if key ==27:
            gerenciador = MDApp.get_running_app().root
            app = MDApp.get_running_app()
            gerenciador.current = str(app.telas[-2])
            return True
        if key == 113:
            app = MDApp.get_running_app()
            print(app.telas)
    