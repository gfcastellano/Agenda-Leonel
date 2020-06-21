from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from urllib import parse
from kivy.network.urlrequest import UrlRequest
from datetime import date
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel

import json


class Adicionar_cliente_tela(Screen):
    dados_clientes=[]
    novo_cliente={}
    popup_error=None
    def on_pre_enter(self):
        print('Entrando em Adicionar_cliente_tela')
        app = MDApp.get_running_app()
        gerenciador = app.root
        app.telas.append(str(gerenciador.current_screen)[14:-2])
        Window.bind(on_keyboard=self.voltar)        
        self.dados_clientes = app.dados_clientes
        self.ids.codigo.text = str(len(self.dados_clientes) + 1)
        self.apagar_infos()

    def apagar_infos(self):
        print('Apagando infos da Adicionar_cliente_tela')
        self.ids.nome_fantasia.text = ''
        self.ids.endereco.text = ''
        self.ids.numero.text = ''
        self.ids.bairro.text = ''
        self.ids.cidade.text = ''
        self.ids.telefone_fixo.text = ''
        self.ids.perfil_cliente.text = ''
        self.ids.nome_1.text = ''
        self.ids.telefone_1.text = ''
        self.ids.tipo_1.text = ''
        self.ids.nome_2.text = ''
        self.ids.telefone_2.text = ''
        self.ids.tipo_2.text = ''
        self.ids.nome_3.text = ''
        self.ids.telefone_3.text = ''
        self.ids.tipo_3.text = ''
        self.ids.banho.active = False
        self.ids.tosa.active = False
        self.ids.pet_shop.active = False
        self.ids.clinica.active = False
        self.ids.razao_social.text = ''
        self.ids.cnpj.text = ''
        self.ids.cep.text = ''

    def adicionar(self):
        novo_cliente={}

        novo_cliente['codigo']         = self.ids.codigo.text
        novo_cliente['nome_fantasia']  = self.ids.nome_fantasia.text
        novo_cliente['endereco']       = self.ids.endereco.text
        novo_cliente['numero']         = self.ids.numero.text
        novo_cliente['bairro']         = self.ids.bairro.text
        novo_cliente['cidade']         = self.ids.cidade.text
        novo_cliente['telefone_fixo']  = self.ids.telefone_fixo.text
        novo_cliente['perfil_cliente'] = self.ids.perfil_cliente.text
        novo_cliente['nome_1']         = self.ids.nome_1.text
        novo_cliente['telefone_1']     = self.ids.telefone_1.text
        novo_cliente['tipo_1']         = self.ids.tipo_1.text
        novo_cliente['nome_2']         = self.ids.nome_2.text
        novo_cliente['telefone_2']     = self.ids.telefone_2.text
        novo_cliente['tipo_2']         = self.ids.tipo_2.text
        novo_cliente['nome_3']         = self.ids.nome_3.text
        novo_cliente['telefone_3']     = self.ids.telefone_3.text
        novo_cliente['tipo_3']         = self.ids.tipo_3.text
        novo_cliente['data']           = str(date.today())
        novo_cliente['razao_social']   = self.ids.razao_social.text
        novo_cliente['cnpj']           = self.ids.cnpj.text
        novo_cliente['cep']            = self.ids.cep.text

        novo_cliente['banho']          = self.ids.banho.active
        novo_cliente['tosa']           = self.ids.tosa.active
        novo_cliente['pet_shop']       = self.ids.pet_shop.active
        novo_cliente['clinica']        = self.ids.clinica.active

        novo_cliente['cliente']        = ''
        novo_cliente['therapet']       = ''
        novo_cliente['tesoura']        = ''
        novo_cliente['tap_higienico']  = ''

        endereco_completo = novo_cliente['endereco'] + ', ' + novo_cliente['numero'] + ' - ' + novo_cliente['bairro'] + ' - ' + novo_cliente['cidade']
        endereco = parse.quote(endereco_completo)
        api_key ='9V2b8ciJf0K3pqhOB2CahsBkpMYuPJKGHhRabS2-iwY'
        url = 'https://geocode.search.hereapi.com/v1/geocode?q=%s&apiKey=%s'%(endereco,api_key)
        app = MDApp.get_running_app()
        app.popup_leituradados.open()
        self.novo_cliente = novo_cliente
        req = UrlRequest(url,on_success=self.success, on_error=self.error, on_failure=self.failure)


    def success(self,urlrequest, result):
        print('Success')
        print('tamanho de result:',len(result['items']))
        
        if len(result['items']) == 0:
            app = MDApp.get_running_app()
            app.popup_leituradados.dismiss()
            self.abrir_popup_error()
        else:
            try:
                print(result['items'][0]['access'][0]['lat'])
                print(result['items'][0]['access'][0]['lng'])
                self.novo_cliente['lat'] = result['items'][0]['access'][0]['lat']
                self.novo_cliente['lon'] = result['items'][0]['access'][0]['lng']
            except KeyError:
                app = MDApp.get_running_app()
                app.popup_leituradados.dismiss()
                self.abrir_popup_error()

        self.dados_clientes.append(self.novo_cliente)
        with open('clientes.json', 'w') as data:
            json.dump(self.dados_clientes,data)

        app = MDApp.get_running_app()
        app.popup_leituradados.dismiss()
        app.root.transition.direction = 'right'
        app.root.current = 'Menu_tela'

    def error(self,urlrequest, result):
        print('Error')
        app = MDApp.get_running_app()
        app.popup_leituradados.dismiss()
        self.abrir_popup_error()
        

        self.dados_clientes.append(self.novo_cliente)
        with open('clientes.json', 'w') as data:
            json.dump(self.dados_clientes,data)

        
        app.root.transition.direction = 'right'
        app.root.current = 'Menu_tela'

    def failure(self,urlrequest, result):
        self.error(urlrequest, result)


    def abrir_popup_error(self):
        if not self.popup_error:
            self.popup_error = MDDialog( size_hint = [0.8,0.8],
                title= 'ERRO',
                text = ('As informações foram armazenadas mas houve um erro ao tentar conseguir as coordenadas geográficas para o endereço digitado.' \
                        ' \n'
                        'Não será possivel colocar um marcador para esse cliente no mapa.'),
                buttons=[MDRaisedButton(
                        text="OK", text_color=MDApp.get_running_app().theme_cls.primary_color, on_release = self.fechar
                    ),
                    MDLabel(
                        text='')
                ],
            )
        self.popup_error.open()


    def fechar(self,*args):
        self.popup_error.dismiss()



    def voltar(self,window,key,*args):
        if key ==27:
            gerenciador = MDApp.get_running_app().root
            app = MDApp.get_running_app()
            gerenciador.transition.direction = 'left'
            gerenciador.current = str(app.telas[-2])
            gerenciador.transition.direction = 'right'
            try:
                if app.telas[-1] == app.telas[-3]:
                    app.telas = app.telas[:-2]
            except IndexError:
                app.telas = app.telas[:-1]
            return True
        if key == 113:
            app = MDApp.get_running_app()
            print(app.telas)

    def voltar_toolbar(self):
        gerenciador = MDApp.get_running_app().root
        app = MDApp.get_running_app()
        gerenciador.transition.direction = 'left'
        gerenciador.current = str(app.telas[-2])
        gerenciador.transition.direction = 'right'
        try:
            if app.telas[-1] == app.telas[-3]:
                app.telas = app.telas[:-2]
        except IndexError:
            app.telas = app.telas[:-1]
