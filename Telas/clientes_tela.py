from kivymd.app import MDApp
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivy.core.window import Window






class Clientes_tela(Screen):
    dados_clientes=[]

    def on_pre_enter(self):
        print('Entrando em Clientes_tela')
        app = MDApp.get_running_app()
        app.registrar_tela()
        Window.bind(on_keyboard=app.voltar)
        
        self.dados_clientes = app.dados_clientes
        
        children = MDApp.get_running_app().root.get_screen('Clientes_tela').ids.box_scroll.children
        if len(children) < 1:
            self.adicionar_clientes(self.dados_clientes)

    def adicionar_clientes(self,dados_clientes):
        print('Adicionando clientes na tela Clientes_tela')
        scroll = MDApp.get_running_app().root.get_screen('Clientes_tela').ids.box_scroll
        if len(dados_clientes) == 0: #Caso ele receba um match que contem nada
            scroll.add_widget(MDLabel(text='Nenhum resultado encontrado',size_hint_y = None, height = 200, halign = 'center'))      
        for cliente in dados_clientes:
            scroll.add_widget(Cliente(codigo = str(cliente['codigo']),nome_fantasia = cliente['nome_fantasia']))

    def mostrar_popup(self):
        MDApp.get_running_app().popup_leituradados.open()
        Clock.schedule_once(self.buscar,0.1)

    def apagar_texto(self):
        self.ids.buscar.text = ''


    def buscar(self,*args):
        print('Excutando busca')
        texto = MDApp.get_running_app().root.get_screen('Clientes_tela').ids.buscar.text
        print('Buscando pelo texto:',texto)
        try:  #Se conseguir transformar em int significa que é pra procurar pelo código
            texto = int(texto)
            texto = str(texto) #se manter no formato int não é possivel iterar
            parametro = 'codigo'
        except ValueError:
            texto = str(texto)
            parametro = 'nome_fantasia'
        self.executar_busca(texto.lower(),parametro)

    def executar_busca(self,texto,parametro):
        print('[executar_busca] texto:',texto)
        print('[executar_busca] parametro:',parametro)
        match=[]
        for cliente in self.dados_clientes:
            if parametro == 'codigo':
                if texto in str(cliente['codigo']):
                    match.append(cliente)
            else:
                if texto in str(cliente['nome_fantasia']).lower():
                    match.append(cliente)

        print('MATCH:',len(match))
        self.apagar_clientes()
        self.adicionar_clientes(match)
        self.fechar_popup()

    def fechar_popup(self):
        MDApp.get_running_app().popup_leituradados.dismiss()

    def apagar_clientes(self):
        MDApp.get_running_app().root.get_screen('Clientes_tela').ids.box_scroll.clear_widgets()
    

        


class Cliente(BoxLayout):
    def __init__(self, codigo='', nome_fantasia='',**kwargs):
        super().__init__(**kwargs)
        self.ids.codigo.text = codigo
        self.ids.nome_fantasia.text = nome_fantasia

    def ir_para_infos(self, root):
        app = MDApp.get_running_app()
        app.root.current = 'Info_tela'
        app.root.get_screen('Info_tela').adicionar_infos(root)




