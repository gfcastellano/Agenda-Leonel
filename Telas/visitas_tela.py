from kivymd.app import MDApp 
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivy.core.window import Window

class Visitas_tela(Screen):
    def on_pre_enter(self):
        print('Entrando em Visitas_tela')
        app = MDApp.get_running_app()
        app.registrar_tela()
        Window.bind(on_keyboard=app.voltar)
        
        self.dados_clientes = app.dados_clientes
        self.dados_visitas  = app.dados_visitas

        self.adicionar_visitas(self.dados_visitas)


    def adicionar_visitas(self, dados_visitas):
        print('Adicionando visitas na tela Visitas_tela')
        scroll = MDApp.get_running_app().root.get_screen('Visitas_tela').ids.box_scroll
        if len(dados_visitas) == 0: #Caso ele receba um match que contem nada
            scroll.add_widget(MDLabel(text='Nenhum resultado encontrado',size_hint_y = None, height = 200, halign = 'center'))      
        for visita in reversed(dados_visitas):
            #print(visita)
            dia  = visita['data'][-2:]
            mes  = visita['data'][-5:-3]
            ano  = visita['data'][-10:-6]
            data = dia + '/' + mes + '/' + ano
            scroll.add_widget(Visita(data = data,
                                     codigo = str(visita['codigo']),
                                     nome_fantasia = visita['nome_fantasia'],
                                     contato = visita['contato'],
                                     informacoes = visita['informacoes']))




class Visita(MDCard):
    def __init__(self,data='', codigo='', nome_fantasia='',contato='', informacoes='',**kwargs):
        super().__init__(**kwargs)
        self.ids.data.text          = data
        self.ids.codigo.text        = codigo
        self.ids.nome_fantasia.text = nome_fantasia
        self.ids.contato.text       = contato
        self.ids.informacoes.text   = informacoes

