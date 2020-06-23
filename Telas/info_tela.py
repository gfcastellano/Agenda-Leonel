from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from urllib import parse
from kivy.core.clipboard import Clipboard
from mapview import MapMarkerPopup


class Info_tela(Screen):
    dados_clientes=[]
    popup_maps=None

    def on_pre_enter(self):
        print('Entrando em Info_tela')
        app = MDApp.get_running_app()
        self.dados_clientes = app.dados_clientes
        app.registrar_tela()
        Window.bind(on_keyboard=app.voltar)

    def apagar_infos(self):
        print('Apagando infos da Info_tela')
        self.ids.codigo.text = ''
        self.ids.nome_fantasia.text = ''
        self.ids.endereco.text = ''
        self.ids.numero.text = ''
        self.ids.bairro.text = ''
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
        self.ids.therapet.active = False
        self.ids.tesoura.active = False
        self.ids.tap_higienico.active = False
    
    def adicionar_infos(self,root):
        dados=[]
        print('Adicionando infos a Info_tela')
        if str(type(root)) == "<class 'kivy.weakproxy.WeakProxy'>":
            nome_fantasia = str(root.ids.nome_fantasia.text)
            dados=''
            print('Adicionando informações do cliente:', nome_fantasia)
            for cliente in self.dados_clientes:
                if nome_fantasia == cliente['nome_fantasia']:
                    dados = cliente
        else:
            lat = str(root)
            dados=''
            print('Adicionando informações do cliente na latitude:', lat)
            for cliente in self.dados_clientes:
                if lat == str(cliente['lat']):
                    dados = cliente
           
        self.ids.codigo.text        = str(dados['codigo'])
        self.ids.nome_fantasia.text = str(dados['nome_fantasia'])
        self.ids.endereco.text      = str(dados['endereco'])
        self.ids.numero.text        = str(dados['numero'])
        self.ids.bairro.text        = str(dados['bairro'])
        self.ids.telefone_fixo.text = str(dados['telefone_fixo'])
        self.ids.perfil_cliente.text= str(dados['perfil_cliente'])
        self.ids.nome_1.text        = str(dados['nome_1'])
        self.ids.telefone_1.text    = str(dados['telefone_1'])
        self.ids.tipo_1.text        = str(dados['tipo_1'])
        self.ids.nome_2.text        = str(dados['nome_2'])
        self.ids.telefone_2.text    = str(dados['telefone_2'])
        self.ids.tipo_2.text        = str(dados['tipo_2'])
        self.ids.nome_3.text        = str(dados['nome_3'])
        self.ids.telefone_3.text    = str(dados['telefone_3'])
        self.ids.tipo_3.text        = str(dados['tipo_3'])
        self.ids.razao_social.text  = str(dados['razao_social'])
        self.ids.cnpj.text          = str(dados['cnpj'])
        self.ids.cep.text           = str(dados['cep'])

        x = (lambda a: 'Sim' if a == 'True' else '')

        self.ids.therapet.text    = x(str(dados['therapet']))
        self.ids.tesoura.text     = x(str(dados['tesoura']))
        self.ids.tap_higienico.text = x(str(dados['tap_higienico']))
        self.ids.banho.text       = x(str(dados['banho']))
        self.ids.tosa.text        = x(str(dados['tosa']))
        self.ids.pet_shop.text    = x(str(dados['pet_shop']))
        self.ids.clinica.text     = x(str(dados['clinica']))

    def abrir_popup_maps(self):    
        if not self.popup_maps:
            self.popup_maps = MDDialog( size_hint = [0.8,0.8],
                text="Deseja ir para rotas no Maps?",
                buttons=[MDRaisedButton(
                        text="SIM", text_color=MDApp.get_running_app().theme_cls.primary_color, on_release = self.abrir_maps
                    ),
                    MDLabel(
                        text='')
                ],
            )
        self.popup_maps.open()
    
    def abrir_maps(self,*args):
        import webbrowser
        print('Abrindo Google Maps')
        endereco = self.ids.endereco.text
        numero = self.ids.numero.text
        bairro = self.ids.bairro.text
        endereco_completo = endereco + ', ' + numero + ' - ' + bairro
        print(endereco_completo)
        endereco_completo = parse.quote(endereco_completo)
        url_maps = 'https://www.google.com.br/maps/dir//'
        url = url_maps + endereco_completo
        print(url)
        webbrowser.open(url)
        self.popup_maps.dismiss()

    def copiar(self,ref):
        toast('Numero copiado')
        numero_copiado = ref.text
        print(numero_copiado)
        Clipboard.copy(numero_copiado)

    def fechar_popup_copiar(self,*args):
        self.cop.dismiss()

    def ir_para_mapa(self):
        for cliente in self.dados_clientes:
            if cliente['nome_fantasia'] == self.ids.nome_fantasia.text:
                dados = cliente
        try:
            lat,lon = dados['lat'], dados['lon']
            app = MDApp.get_running_app()
            mapa_tela = app.root.get_screen('Mapa_tela')
            mapa_tela.ids.mapa.center_on(lat,lon)
            mapa_tela.ids.mapa.zoom = 16
            print('Indo para Mapa_tela centralizado em:', self.ids.nome_fantasia.text)
            app.root.transition.direction = 'right'
            app.root.current = 'Mapa_tela'
        except:
            pass
        

