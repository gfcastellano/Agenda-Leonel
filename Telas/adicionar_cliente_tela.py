from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from urllib import parse
from kivy.network.urlrequest import UrlRequest
from datetime import date
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from pprint import pprint

import json


class Adicionar_cliente_tela(Screen):
    dados_clientes=[]
    novo_cliente={}
    popup_error=None
    popup_cnpj=None
    popup_infos = None
    def on_pre_enter(self):
        print('Entrando em Adicionar_cliente_tela')
        app = MDApp.get_running_app()
        app.registrar_tela()
        Window.bind(on_keyboard=app.voltar)        
        self.dados_clientes = app.dados_clientes
        self.ids.codigo.text = str(len(self.dados_clientes) + 1)
        self.apagar_infos()
        self.ids.scroll.scroll_y=1

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
        nome       = self.ids.nome_fantasia.text
        endereco   = self.ids.endereco.text
        numero     = self.ids.numero.text
        bairro     = self.ids.bairro.text
        cidade     = self.ids.cidade.text

        #print('Nome:',nome)
        #print('endereco:',endereco)
        #print('numero:',numero)
        #print('bairro:',bairro)
        #print('cidade:',cidade)

        if nome == '' or endereco == '' or numero == '' or bairro == '' or cidade == '':
            self.abrir_popup_infos()
            print('Entrou no if')
        else:
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

            novo_cliente['cliente']        = False
            novo_cliente['therapet']       = False
            novo_cliente['tesoura']        = False
            novo_cliente['tap_higienico']  = False

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
        pprint(result)
        
        if len(result['items']) == 0:
            app = MDApp.get_running_app()
            app.popup_leituradados.dismiss()
            self.abrir_popup_error()
        else:
            try:
                print(result['items'][0]['access'][0]['lat'])
                print(result['items'][0]['access'][0]['lng'])
                print('Postal Code:',result['items'][0]['address']['postalCode'])
                self.novo_cliente['lat'] = result['items'][0]['access'][0]['lat']
                self.novo_cliente['lon'] = result['items'][0]['access'][0]['lng']
                self.novo_cliente['cep'] = result['items'][0]['address']['postalCode']
            except KeyError: #Caso ele tente acessar algum valor do result e não consiga
                app = MDApp.get_running_app()
                app.popup_leituradados.dismiss()
                self.abrir_popup_error()

        # Colocar novos dados na base de dados
        app = MDApp.get_running_app()
        app.patch(self.novo_cliente)
        # Requisitar dados novos
        app.get()
        # Adicionar novo marcador ao mapa
        #app.root.get_screen('Mapa_tela').verificar_marcadores()
        # Repopular a tela anterior
        app.root.get_screen('Info_tela').adicionar_infos(self.ids.codigo.text)
        # Fecha o popup
        app.popup_leituradados.dismiss()
        # Volta para tela anterior
        app.root.transition.direction = 'right'
        app.root.current = 'Menu_tela'

    def error(self,urlrequest, result):
        print('Error')
        app = MDApp.get_running_app()
        app.popup_leituradados.dismiss()
        self.abrir_popup_error()
        

        """ self.dados_clientes.append(self.novo_cliente)
        app = MDApp.get_running_app()
        with open(app.path + 'clientes.json', 'w') as data:
            json.dump(self.dados_clientes,data) """

        
        app.root.transition.direction = 'right'
        app.root.current = 'Menu_tela'

    def failure(self,urlrequest, result):
        self.error(urlrequest, result)


    def abrir_popup_error(self):
        if not self.popup_error:
            self.popup_error = MDDialog( size_hint = [0.8,0.8],
                title= 'ERRO',
                text = ('As informações NÃO foram armazenadas , houve um erro ao tentar conseguir as coordenadas geográficas e o CEP para o endereço digitado.' \
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


    def consulta_cnpj(self):
        url = 'https://www.receitaws.com.br/v1/cnpj/'
        cnpj = str(self.ids.cnpj.text)
        cnpj = cnpj.replace(".",'').replace(',','').replace('/','').replace('-','') # Para que fique somente os numeros
        print(cnpj)
        url_cnpj = url + cnpj
        UrlRequest(url_cnpj, on_success=self.success_cnpj)

    def success_cnpj(self,urlrequest, result):
        print('Tamanho do resultado:', len(result))
        pprint(result) # Para auxiliar no debug
        if len(result) > 2: # Significa que deu certo
            self.ids.nome_fantasia.text = str(result['fantasia'])
            self.ids.endereco.text      = str(result['logradouro'])
            self.ids.numero.text        = str(result['numero'])
            self.ids.bairro.text        = str(result['bairro'])
            self.ids.cidade.text        = str(result['municipio'])
            self.ids.telefone_fixo.text = str(result['telefone'])
            self.ids.razao_social.text  = str(result['nome'])
            self.ids.cep.text           = str(result['cep'])

        else:
            if not self.popup_cnpj:
                self.popup_cnpj = MDDialog( size_hint = [0.8,0.8],
                    title= str(result['message']),
                    text = ('Não foi possivel achar informações sobre esse CNPJ, confira se não há erro de digitação'),
                    buttons=[MDRaisedButton(
                            text="OK", text_color=MDApp.get_running_app().theme_cls.primary_color, on_release = self.fechar_cnpj
                        ),
                        MDLabel(
                            text='')
                    ],
                )
            self.popup_cnpj.open()
            print('erro')

    def fechar_cnpj(self,*args):
        self.popup_cnpj.dismiss()
    
    def abrir_popup_infos(self):
        if not self.popup_infos:
            self.popup_infos = MDDialog( size_hint = [0.8,0.8],
                title= 'ERRO',
                text = ('Há informações que necessitam ser inseridas.' \
                        ' \n' 
                        'Verifique se foram inseridos: \n'
                        ' - Nome \n' 
                        ' - Endereço \n' 
                        ' - Numero \n' 
                        ' - Bairro \n' 
                        ' - Cidade'),
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