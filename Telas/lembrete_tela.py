from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivymd.uix.picker import MDDatePicker
from datetime import date
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineAvatarListItem
from kivy.properties import StringProperty
from kivy.clock import Clock

import json
from pprint import pprint



class Lembrete_tela(Screen):
    popup_pesquisa_cliente=None
    popup_pesquisa_contato=None
    popup_pesquisa_visita=None
    popup_infos=None

    def on_pre_enter(self):
        print('Entrando em Cliente_tela')
        app = MDApp.get_running_app()
        app.registrar_tela()
        Window.bind(on_keyboard=app.voltar)
        
        self.dados_clientes = app.dados_clientes
        self.dados_visitas  = app.dados_visitas
        self.dados_lembretes = app.dados_lembretes


        #data = date.today()
        #self.primeiro_dia = str(data.day) if len(str(data.day)) > 1 else '0'+str(data.day)
        #self.primeiro_mes = str(data.month) if len(str(data.month)) > 1 else '0'+str(data.month)
        #self.primeiro_ano = str(data.year)
        #self.ids.data.text = self.primeiro_dia + '/' + self.primeiro_mes + '/' + self.primeiro_ano

    def adicionar_infos(self,objeto):
        print(objeto)
        print(type(objeto))
        print(objeto.nome_fantasia)
        #self.ids.data.text    = objeto.ids.data.text
        #self.ids.codigo.text  = objeto.ids.codigo.text
        self.ids.nome_fantasia.text    = objeto.ids.nome_fantasia.text
        #self.ids.contato.text    = objeto.ids.contato.text
        #self.ids.informacoes.text    = objeto.ids.informacoes.text
        #self.ids.visita.text    = objeto.ids.visita.text
        self.ids.identificador.text    = objeto.ids.identificador.text
        self.ids.lembrete.text    = objeto.ids.lembrete.text

    def limpar(self):
        data = date.today()
        self.primeiro_dia = str(data.day) if len(str(data.day)) > 1 else '0'+str(data.day)
        self.primeiro_mes = str(data.month) if len(str(data.month)) > 1 else '0'+str(data.month)
        self.primeiro_ano = str(data.year)
        #self.ids.data.text = self.primeiro_dia + '/' + self.primeiro_mes + '/' + self.primeiro_ano
        self.ids.nome_fantasia.text    = ''
        #self.ids.contato.text    = ''
        #self.ids.informacoes.text    = ''
        #self.ids.visita.text    = ''
        self.ids.lembrete.text    = ''
        self.ids.data_lembrete.text    = ''

    def abrir_popup_data(self):
        primeiro_calendario = MDDatePicker(callback = self.marcar_data_visita)
        primeiro_calendario.open()

    def marcar_data_visita(self, data):
        self.primeiro_dia = str(data.day) if len(str(data.day)) > 1 else '0'+str(data.day)
        self.primeiro_mes = str(data.month) if len(str(data.month)) > 1 else '0'+str(data.month)
        self.primeiro_ano = str(data.year)
        self.ids.data.text = self.primeiro_dia + '/' + self.primeiro_mes + '/' + self.primeiro_ano

    def abrir_popup_data_lembrete(self):
        primeiro_calendario = MDDatePicker(callback = self.marcar_data_lembrete)
        primeiro_calendario.open()

    def marcar_data_lembrete(self, data):
        self.primeiro_dia = str(data.day) if len(str(data.day)) > 1 else '0'+str(data.day)
        self.primeiro_mes = str(data.month) if len(str(data.month)) > 1 else '0'+str(data.month)
        self.primeiro_ano = str(data.year)
        self.ids.data_lembrete.text = self.primeiro_dia + '/' + self.primeiro_mes + '/' + self.primeiro_ano

    def mostrar_popup(self):
        MDApp.get_running_app().popup_leituradados.open()
        Clock.schedule_once(self.pesquisar_cliente,0.1)

    def pesquisar_cliente(self,*args):
        MDApp.get_running_app().popup_leituradados.dismiss()
        print('Executando pesquisar_cliente')
        texto = self.ids.nome_fantasia.text
        texto = str(texto).lower()
        match=[]
        for cliente in self.dados_clientes:
            if texto in str(cliente['nome_fantasia']).lower():
                match.append(cliente)
        items=[]
        for cliente in match:
            items.append(Item_cliente_lembrete(text=cliente['nome_fantasia']))

        #if not self.popup_pesquisa_cliente:
        self.popup_pesquisa_cliente = MDDialog(
            title="Clientes",
            type="simple",
            items=items)
        self.popup_pesquisa_cliente.open()

    def pesquisar_contato(self):
        print('Executando pesquisar_contato')
        texto = self.ids.nome_fantasia.text
        items=[]
        for cliente in self.dados_clientes:
            if texto == cliente['nome_fantasia']:
                dados = cliente
                nome_1, nome_2, nome_3= dados['nome_1'], dados['nome_2'], dados['nome_3']

                
                for nome in [nome_1, nome_2, nome_3]:
                    if len(nome) != 0:
                        items.append(Item_contato_lembrete(text=nome))
        self.popup_pesquisa_contato = MDDialog(
            title="Contatos cadastrados para esse cliente",
            type="simple",
            items=items)
        self.popup_pesquisa_contato.open()

    def pesquisar_visita(self):
        print('Executando pesquisar_visita')
        items=[Item_visita_lembrete(text='Presencial'),Item_visita_lembrete(text='Ligação'),Item_visita_lembrete(text="Whats"),Item_visita_lembrete(text="E-mail")]
        
        self.popup_pesquisa_visita = MDDialog(
            title="Tipos de visita",
            type="simple",
            items=items)
        self.popup_pesquisa_visita.open()

    def adicionar_lembrete(self):

        MDApp.get_running_app().popup_leituradados.open()
        Clock.schedule_once(self.adicionando_cliente_ao_firebase,0.1)

    def adicionando_cliente_ao_firebase(self,*args):
        print("Execuntando adicionar_lembrete")
        novo_visita={}
        #data       = self.ids.data.text
        nome_fantasia   = self.ids.nome_fantasia.text
        #contato     = self.ids.contato.text
        #visita     = self.ids.visita.text
        identificador = self.ids.identificador.text
        #informacoes     = self.ids.informacoes.text
        lembrete        =self.ids.lembrete.text
        #pergunta_lembrete = self.ids.pergunta_lembrete.state
        data_lembrete = self.ids.data_lembrete.text
        


        if nome_fantasia == '' or lembrete == '' or data_lembrete == '':
            self.abrir_popup_infos()
            print('Não existem os dados mínimos necessários, não salvando as alterações')
        else:
            print("Existem dados mínimos necessários para adicionar lembrete")
            #novo_visita['data']            = data
            novo_visita['nome_fantasia']   = nome_fantasia
            #novo_visita['contato']         = contato
            #novo_visita['visita']          = visita
            #novo_visita['informacoes']     = informacoes
            novo_visita['identificador']   = identificador
            novo_visita['lembrete']        = lembrete 
            #novo_visita['pergunta_lembrete']   = pergunta_lembrete
            novo_visita['data_lembrete']   = data_lembrete
            
            #self.novo_visita = novo_visita

            #self.dados_visitas.append(self.novo_visita)
            #pprint(novo_visita)

            # Colocar dados no Firebase
            app = MDApp.get_running_app()
            app.patch(novo_visita)
            # Requisitar dados novos
            app.get()
            # Repopular a tela anterior
            #if app.root.get_screen('Lembretes_tela').ids.buscar.text != '':
            app.root.get_screen('Lembretes_tela').buscar()
            # Voltar a tela anterior
            app.root.transition.direction = 'right'
            app.root.current = app.telas[-2] # 'Lembretes_tela'
    def abrir_popup_infos(self):
        if not self.popup_infos:
            self.popup_infos = MDDialog( size_hint = [0.8,0.8],
                title= 'ERRO',
                text = ('Há informações que necessitam ser inseridas.' \
                        ' \n' 
                        'Verifique se foram inseridos: \n'
                        ' - nome_fantasia \n' 
                        ' - lembrete \n' 
                        ' - data_lembrete \n' ),
                        #' - Bairro \n' 
                        #' - Cidade'),
                buttons=[MDRaisedButton(
                        text="OK", text_color=MDApp.get_running_app().theme_cls.primary_color, on_release = self.fechar_info
                    ),
                    MDLabel(
                        text='')
                ],
            )
        self.popup_infos.open()

    def fechar_info(self, *args):
        self.popup_infos.dismiss()

    def adicionar_nome_fantasia(self):
        app = MDApp.get_running_app()
        nome_fantasia = app.root.get_screen('Info_tela').ids.info_tab.ids.nome_fantasia.text
        self.ids.nome_fantasia.text = nome_fantasia
        
        data = date.today()
        self.primeiro_dia = str(data.day) if len(str(data.day)) > 1 else '0'+str(data.day)
        self.primeiro_mes = str(data.month) if len(str(data.month)) > 1 else '0'+str(data.month)
        self.primeiro_ano = str(data.year)
        self.ids.data.text = self.primeiro_dia + '/' + self.primeiro_mes + '/' + self.primeiro_ano

    
class Item_cliente_lembrete(OneLineAvatarListItem):
    divider = None
    source = StringProperty()

    def preencher_cliente(self,text):
        print('Executando preencher_cliente')
        MDApp.get_running_app().root.get_screen('Lembrete_tela').ids.nome_fantasia.text = text

class Item_contato_lembrete(OneLineAvatarListItem):
    divider = None
    source = StringProperty()

    def preencher_contato(self,text):
        print('Executando preencher_contato')
        MDApp.get_running_app().root.get_screen('Lembrete_tela').ids.contato.text = text

class Item_visita_lembrete(OneLineAvatarListItem):
    divider = None
    source = StringProperty()

    def preencher_visita(self,text):
        print('Executando preencher_visita')
        MDApp.get_running_app().root.get_screen('Lembrete_tela').ids.visita.text = text