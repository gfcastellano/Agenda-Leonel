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



class Visita_tela(Screen):
    popup_pesquisa_cliente=None
    popup_pesquisa_contato=None

    def on_pre_enter(self):
        print('Entrando em Visita_tela')
        app = MDApp.get_running_app()
        app.registrar_tela()
        Window.bind(on_keyboard=app.voltar)
        
        self.dados_clientes = app.dados_clientes
        self.dados_visitas  = app.dados_visitas
        #data = date.today()
        #self.primeiro_dia = str(data.day) if len(str(data.day)) > 1 else '0'+str(data.day)
        #self.primeiro_mes = str(data.month) if len(str(data.month)) > 1 else '0'+str(data.month)
        #self.primeiro_ano = str(data.year)
        #self.ids.data.text = self.primeiro_dia + '/' + self.primeiro_mes + '/' + self.primeiro_ano
    def adicionar_infos(self,objeto):
        self.ids.data.text    = objeto.ids.data.text
        #self.ids.codigo.text  = objeto.ids.codigo.text
        self.ids.nome_fantasia.text    = objeto.ids.nome_fantasia.text
        self.ids.contato.text    = objeto.ids.contato.text
        self.ids.informacoes.text    = objeto.ids.informacoes.text
        self.ids.visita.text    = objeto.ids.visita.text

    def limpar(self):
        data = date.today()
        self.primeiro_dia = str(data.day) if len(str(data.day)) > 1 else '0'+str(data.day)
        self.primeiro_mes = str(data.month) if len(str(data.month)) > 1 else '0'+str(data.month)
        self.primeiro_ano = str(data.year)
        self.ids.data.text = self.primeiro_dia + '/' + self.primeiro_mes + '/' + self.primeiro_ano
        self.ids.nome_fantasia.text    = ''
        self.ids.contato.text    = ''
        self.ids.informacoes.text    = ''
        self.ids.visita.text    = ''

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
            items.append(Item_cliente(text=cliente['nome_fantasia']))

        #if not self.popup_pesquisa_cliente:
        self.popup_pesquisa_cliente = MDDialog(
            title="Clientes",
            type="simple",
            items=items)
        self.popup_pesquisa_cliente.open()

    def pesquisar_contato(self):
        print('Executando pesquisar_contato')
        texto = self.ids.nome_fantasia.text
        for cliente in self.dados_clientes:
            if texto == cliente['nome_fantasia']:
                dados = cliente
                nome_1, nome_2, nome_3= dados['nome_1'], dados['nome_2'], dados['nome_3']

                items=[]
                for nome in [nome_1, nome_2, nome_3]:
                    if len(nome) != 0:
                        items.append(Item_contato(text=nome))
        self.popup_pesquisa_contato = MDDialog(
            title="Contatos cadastrados para esse cliente",
            type="simple",
            items=items)
        self.popup_pesquisa_contato.open()

    def adicionar_visita(self):
        novo_visita={}
        data       = self.ids.data.text
        nome_fantasia   = self.ids.nome_fantasia.text
        contato     = self.ids.contato.text
        visita     = self.ids.visita.text
        informacoes     = self.ids.informacoes.text


        if data == '' or nome_fantasia == '' or contato == '' or visita == '':
            #self.abrir_popup_infos()
            print('Entrou no if')
        else:
            novo_visita['data']            = self.ids.data.text
            novo_visita['nome_fantasia']         = self.ids.nome_fantasia.text
            novo_visita['contato']         = self.ids.contato.text
            novo_visita['visita']          = self.ids.visita.text
            novo_visita['informacoes']     = self.ids.informacoes.text


            
            self.novo_visita = novo_visita

            self.dados_visitas.append(self.novo_visita)

        app = MDApp.get_running_app()
        with open(app.path + 'visitas.json', 'w') as data:
            json.dump(self.dados_visitas,data)

        app.root.transition.direction = 'right'
        app.root.current = 'Visitas_tela'

    
class Item_cliente(OneLineAvatarListItem):
    divider = None
    source = StringProperty()

    def preencher_cliente(self,text):
        print('Executando preencher_cliente')
        MDApp.get_running_app().root.get_screen('Visita_tela').ids.nome_fantasia.text = text

class Item_contato(OneLineAvatarListItem):
    divider = None
    source = StringProperty()

    def preencher_contato(self,text):
        print('Executando preencher_contato')
        MDApp.get_running_app().root.get_screen('Visita_tela').ids.contato.text = text

    