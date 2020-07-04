from kivymd.app import MDApp 
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.uix.picker import MDDatePicker

class Visitas_tela(Screen):
    dia=''
    mes=''
    ano=''
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

    def mostrar_popup(self):
        MDApp.get_running_app().popup_leituradados.open()
        Clock.schedule_once(self.buscar,0.1)

    def buscar(self,*args):
        print('Excutando busca')
        texto = MDApp.get_running_app().root.get_screen('Visitas_tela').ids.buscar.text
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
        for visita in self.dados_visitas:
            if parametro == 'codigo':
                if texto in str(visita['codigo']):
                    match.append(visita)
            else:
                if texto in str(visita['nome_fantasia']).lower():
                    match.append(visita)

        remover=[]
        if self.ids.data.text != '':
            data = self.ano + '-' + self.mes + '-' + self.dia
            print(data)
            for visita in match:
                if visita['data'] != data:
                    remover.append(visita)
            
        for visita in remover:
            match.remove(visita)
                  
        print('MATCH:',len(match))
        self.apagar_visitas()
        self.adicionar_visitas(match)
        MDApp.get_running_app().root.get_screen('Visitas_tela').ids.box_scroll.scroll_y=1
        self.fechar_popup()

    def apagar_visitas(self):
        MDApp.get_running_app().root.get_screen('Visitas_tela').ids.box_scroll.clear_widgets()

    def fechar_popup(self):
        MDApp.get_running_app().popup_leituradados.dismiss()

    def apagar_texto(self):
        self.ids.buscar.text = ''
    
    def apagar_data(self):
        self.ids.data.text = ''
    
    def abrir_popup_data(self):
        calendario = MDDatePicker(callback = self.data_escolhida)
        calendario.open()

    def data_escolhida(self, data):
        #print(data)
        self.dia = str(data.day) if len(str(data.day)) > 1 else '0'+str(data.day)
        self.mes = str(data.month) if len(str(data.month)) > 1 else '0'+str(data.month)
        self.ano = str(data.year)
        self.ids.data.text = self.dia + '/' + self.mes + '/' + self.ano



class Visita(MDCard):
    def __init__(self,data='', codigo='', nome_fantasia='',contato='', informacoes='',**kwargs):
        super().__init__(**kwargs)
        self.ids.data.text          = data
        self.ids.codigo.text        = codigo
        self.ids.nome_fantasia.text = nome_fantasia
        self.ids.contato.text       = contato
        self.ids.informacoes.text   = informacoes

