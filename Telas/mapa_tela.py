from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from Mapa.marcador import Marcador, Marcador_vermelho
from kivy.core.window import Window

class Mapa_tela(Screen):
    lista_de_marcadores=[]
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
            self.adicionar_marcadores(self.dados_clientes)
        for cliente in self.dados_clientes:
            if cliente['nome_fantasia'] not in self.lista_de_marcadores:
                self.adicionar_marcadores(cliente)
        

    def adicionar_marcadores(self,dados_cliente):
        print('Adicionando marcadores no Mapa')
        for cliente in self.dados_clientes:
            try:
                nome, lat, lon = cliente['nome_fantasia'],cliente['lat'],cliente['lon']
                if nome not in self.lista_de_marcadores:
                    self.ids.mapa.add_widget(Marcador(lat=lat,lon=lon)) #adiciona marcador
                    self.lista_de_marcadores.append(nome) #adiciona nome a lista
            except:
                continue
        
        print('Fim de adicionar_marcadores:',len(self.lista_de_marcadores))
        print(self.lista_de_marcadores[-1])
                

    def voltar(self,window,key,*args):
        if key ==27:
            app = MDApp.get_running_app()
            print('----------------------------------------------------------------------------------Ultima tela:',str(app.telas[-2]))
            if str(app.telas[-2]) == 'Info_tela':
                print('[voltar] if')
                app.root.transition.direction = 'left'                
                app.root.current = str(app.telas[-2])
            else:
                print('[voltar] elif')
                app.root.transition.direction = 'left'
                app.root.current = str(app.telas[-2])
                app.root.transition.direction = 'right'
            try:
                if app.telas[-1] == app.telas[-3]:
                    app.telas = app.telas[:-2]
            except IndexError:
                app.telas = app.telas[:-1]
            return True
        if key == 113:
            app = MDApp.get_running_app()
            print(app.telas)
    

    def on_pre_leave(self):
        mapa = self.ids.mapa
        lat, lon = mapa.lat, mapa.lon