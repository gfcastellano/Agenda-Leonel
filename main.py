import kivy
import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import json



class Gerenciador(ScreenManager):
    pass

class Menu(Screen):
    pass

class Mapa(Screen):
    
    
    def voltar(self,window,key,*args):
        if key == 27:
            App.get_running_app().root.current = 'Menu'
            return True
    
    def on_pre_leave(self):
        Window.unbind(on_keyboard = self.voltar)


class Clientes(Screen):
    #atualizar essa lista automaticamente ao carregar a tela Clientes, na função carregar_clientes
    clientes={}
    print("Print1:",clientes)


    

    def on_pre_enter(self,*args):
        self.carregar_clientes()
        print("Print2:", len(self.clientes))
        Window.bind(on_keyboard = self.voltar)
        self.atualizar_tela_clientes(self.clientes)

    def carregar_clientes(self,*args):
        try:
            with open('Gabriel\Com_base_de_dados\clientes.json', 'r') as data:
                self.clientes = json.load(data)
                print("Achou o arquivo")
        except FileNotFoundError:
            print("Não achou o arquivo")
            pass

    def atualizar_tela_clientes(self,clientes = clientes):
        self.ids.box.clear_widgets()
        self.ids.pesquisar.text = ''
        print('Limpou')
        
        i=0
        while i < len(clientes):
            nome_fantasia = clientes[i]['nome_fantasia']
            self.ids.box.add_widget(Label(text=nome_fantasia,
                                          id=nome_fantasia,
                                          font_size=30, 
                                          size_hint_y=None,
                                          height=200,
                                          )
                                    )  
            i = i + 1                

    def voltar(self,window,key,*args):
        if key == 27:
            App.get_running_app().root.current = 'Menu'
            return True
    
    def on_pre_leave(self):
        Window.unbind(on_keyboard = self.voltar)

    def buscar(self,*args):
        texto_pesquisar = str(self.ids.pesquisar.text)
        print("PRINT texto_pesquisar:", texto_pesquisar)
        match=[]
        for cliente in self.clientes:
            nome_fantasia = cliente['nome_fantasia']
            print("QUAL CLIENTE?:",nome_fantasia)
            if nome_fantasia.find(texto_pesquisar) > -1:
                match.append(cliente)
        print("MATCH:", match)
        ### Atualizar a tela com somente os clientes na lista match
        self.atualizar_tela_clientes(clientes = match)

class Test(App):
	def build(self):
        ### Ler lista de clientes já cadastrados do arquivo .json
		return Gerenciador()
	
if __name__ == '__main__':
    Test().run()