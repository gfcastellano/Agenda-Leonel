from kivymd.app import MDApp 
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton

class Visitas_tela(Screen):
    data={'card-plus-outline': 'Adicionar visita'}
    primeiro_dia=''
    primeiro_mes=''
    primeiro_ano=''
    segundo_dia=''
    segundo_mes=''
    segundo_ano=''
    popup_segunda_data=None
    popup_visita=None

    def on_pre_enter(self):
        print('Entrando em Visitas_tela')
        app = MDApp.get_running_app()
        app.registrar_tela()
        Window.bind(on_keyboard=app.voltar)
        
        self.dados_clientes = app.dados_clientes
        self.dados_visitas  = app.dados_visitas
        if app.telas[-2] == 'Menu_tela':
            self.ids.buscar.text = ''
        self.apagar_visitas()
        self.ids.scroll.scroll_y=1


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

        #Adicionando visitas na visitas_tab
        visitas_tab = MDApp.get_running_app().root.get_screen('Info_tela').ids.visitas_tab.ids.box_scroll
        if len(dados_visitas) == 0: #Caso ele receba um match que contem nada
            visitas_tab.add_widget(MDLabel(text='Nenhum resultado encontrado',size_hint_y = None, height = 200, halign = 'center'))      
        for visita in reversed(dados_visitas):
            #print(visita)
            dia  = visita['data'][-2:]
            mes  = visita['data'][-5:-3]
            ano  = visita['data'][-10:-6]
            data = dia + '/' + mes + '/' + ano
            visitas_tab.add_widget(Visita(data = data,
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
        app = MDApp.get_running_app()
        self.dados_visitas = app.dados_visitas
        for visita in self.dados_visitas:
            if parametro == 'codigo':
                if texto in str(visita['codigo']):
                    match.append(visita)
            else:
                if texto in str(visita['nome_fantasia']).lower():
                    match.append(visita)

        remover=[]
        if self.ids.data.text != '':  #Verifica se tem a condição de data
            if len(self.ids.data.text) > 10: #verifica se tem uma ou duas datas
                if self.ordem == 'primeiro':
                    menor_data = self.primeiro_ano + '-' + self.primeiro_mes + '-' + self.primeiro_dia
                    maior_data = self.segundo_ano + '-' + self.segundo_mes + '-' + self.segundo_dia
                else:
                    maior_data = self.primeiro_ano + '-' + self.primeiro_mes + '-' + self.primeiro_dia
                    menor_data = self.segundo_ano + '-' + self.segundo_mes + '-' + self.segundo_dia
                #print(menor_data, maior_data)
                for visita in match:
                    if int(visita['data'][:4]) < int(menor_data[:4]): #verificando ano
                        remover.append(visita)
                    else:
                        if int(visita['data'][:4]) == int(menor_data[:4]) and \
                           int(visita['data'][5:7]) < int(menor_data[5:7]):  #verificando mes
                            if visita in remover:
                                continue
                            else:
                                remover.append(visita)
                        else:
                            if int(visita['data'][:4]) == int(menor_data[:4]) and \
                               int(visita['data'][5:7]) == int(menor_data[5:7]) and \
                               int(visita['data'][8:]) < int(menor_data[8:]): #verificando dia
                                if visita in remover:
                                    continue
                                else:
                                    remover.append(visita)
                    if int(visita['data'][:4]) > int(maior_data[:4]): #verificando ano
                        if visita in remover:
                                continue
                        else:
                            remover.append(visita)
                    else:
                        if int(visita['data'][:4]) == int(maior_data[:4]) and \
                           int(visita['data'][5:7]) > int(maior_data[5:7]): #verificando mes
                            if visita in remover:
                                continue
                            else:
                                remover.append(visita)
                        elif int(visita['data'][:4]) == int(maior_data[:4]) and \
                            int(visita['data'][5:7]) == int(maior_data[5:7]) and \
                            int(visita['data'][8:]) > int(maior_data[8:]):                             
                            if visita in remover:
                                continue
                            else:
                                remover.append(visita)
            else: #significa que só tem uma data na busca
                data = self.primeiro_ano + '-' + self.primeiro_mes + '-' + self.primeiro_dia
                #print(data)
                for visita in self.dados_visitas:
                    if visita['data'] != data:
                        remover.append(visita)       
        
        for visita in remover:
            try:
                match.remove(visita)
            except ValueError:
                continue
                  
        print('MATCH:',len(match))
        self.apagar_visitas()
        self.adicionar_visitas(match)
        self.fechar_popup()
        self.ids.scroll.scroll_y=1

    def apagar_visitas(self):
        MDApp.get_running_app().root.get_screen('Visitas_tela').ids.box_scroll.clear_widgets()
        MDApp.get_running_app().root.get_screen('Info_tela').ids.visitas_tab.ids.box_scroll.clear_widgets()

    def fechar_popup(self):
        MDApp.get_running_app().popup_leituradados.dismiss()

    def apagar_texto(self):
        self.ids.buscar.text = ''
        
    
    def apagar_data(self):
        self.ids.data.text = ''
        #Apagar tambem da vsitas_tab
        MDApp.get_running_app().root.get_screen('Info_tela').ids.visitas_tab.ids.data.text = ''
        if str(MDApp.get_running_app().root.current_screen)[14:-2] == 'Info_tela':
            self.buscar()

    def abrir_popup_primeira_data(self):
        primeiro_calendario = MDDatePicker(callback = self.abrir_popup_segunda_data)
        primeiro_calendario.open()

    def abrir_popup_segunda_data(self, data):
        self.primeiro_dia = str(data.day) if len(str(data.day)) > 1 else '0'+str(data.day)
        self.primeiro_mes = str(data.month) if len(str(data.month)) > 1 else '0'+str(data.month)
        self.primeiro_ano = str(data.year)
        self.ids.data.text = self.primeiro_dia + '/' + self.primeiro_mes + '/' + self.primeiro_ano
        if not self.popup_segunda_data:
            app = MDApp.get_running_app()
            self.popup_segunda_data = MDDialog( size_hint = [0.8,0.8],
                text='Deseja escolher uma segunda data?\n\nCaso escolha "Sim" será retornado as visitas que estão no intervalo entre as duas datas escolhidas.',
                buttons=[
                    MDRaisedButton(
                        text="Sim", on_release = self.escolher_segunda_data
                    ),
                    MDFlatButton(
                        text="Não", text_color=MDApp.get_running_app().theme_cls.primary_color, on_release = self.fechar_popup_segunda_data
                    )
                ],
            )
        self.popup_segunda_data.open()
    
    def fechar_popup_segunda_data(self,*args):
        self.popup_segunda_data.dismiss()
        MDApp.get_running_app().root.get_screen('Info_tela').ids.visitas_tab.ids.data.text = self.ids.data.text
        if str(MDApp.get_running_app().root.current_screen)[14:-2] == 'Info_tela':
            self.buscar()
    
    def escolher_segunda_data(self,*args):
        self.popup_segunda_data.dismiss()
        segundo_calendario = MDDatePicker(callback = self.segunda_data)
        segundo_calendario.open()

    def segunda_data(self,date, *args):
        #print(data)
        self.segundo_dia = str(date.day) if len(str(date.day)) > 1 else '0'+str(date.day)
        self.segundo_mes = str(date.month) if len(str(date.month)) > 1 else '0'+str(date.month)
        self.segundo_ano = str(date.year)
        
        if int(self.primeiro_ano) == int(self.segundo_ano):
            if int(self.primeiro_mes) == int(self.segundo_mes):
                if int(self.primeiro_dia) == int(self.segundo_dia):
                    pass
                elif int(self.primeiro_dia) < int(self.segundo_dia):
                    self.ids.data.text = self.ids.data.text + ' até ' + self.segundo_dia + '/' + self.segundo_mes + '/' + self.segundo_ano
                    self.ordem = 'primeiro'
                else:
                    self.ids.data.text = self.segundo_dia + '/' + self.segundo_mes + '/' + self.segundo_ano + ' até ' +  self.ids.data.text
                    self.ordem = 'segundo'
            elif int(self.primeiro_mes) < int(self.segundo_mes):
                self.ids.data.text = self.ids.data.text + ' até ' + self.segundo_dia + '/' + self.segundo_mes + '/' + self.segundo_ano
                self.ordem = 'primeiro'
            else:
                self.ids.data.text = self.segundo_dia + '/' + self.segundo_mes + '/' + self.segundo_ano + ' até ' +  self.ids.data.text
                self.ordem = 'segundo'
        elif int(self.primeiro_ano) < int(self.segundo_ano):
            self.ids.data.text = self.ids.data.text + ' até ' + self.segundo_dia + '/' + self.segundo_mes + '/' + self.segundo_ano
            self.ordem = 'primeiro'
        else:
            self.ids.data.text = self.segundo_dia + '/' + self.segundo_mes + '/' + self.segundo_ano + ' até ' +  self.ids.data.text
            self.ordem = 'segundo'
        
        MDApp.get_running_app().root.get_screen('Info_tela').ids.visitas_tab.ids.data.text = self.ids.data.text
        if str(MDApp.get_running_app().root.current_screen)[14:-2] == 'Info_tela':
            self.buscar()

    def ir_para_visita_tela(self):
        app = MDApp.get_running_app()
        app.root.current = 'Visita_tela'
        print('Executou')

    def abrir_popup_visita(self):    
        if not self.popup_visita:
            self.popup_visita = MDDialog(
                title="Visita",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL"
                    ),
                    MDFlatButton(
                        text="OK"
                    ),
                ],
            )
        self.popup_visita.open()
        



class Visita(MDCard):
    def __init__(self,data='', codigo='', nome_fantasia='',contato='', informacoes='',**kwargs):
        super().__init__(**kwargs)
        self.ids.data.text          = data
        self.ids.codigo.text        = codigo
        self.ids.nome_fantasia.text = nome_fantasia
        self.ids.contato.text       = contato
        self.ids.informacoes.text   = informacoes


class Content(BoxLayout):
    pass
