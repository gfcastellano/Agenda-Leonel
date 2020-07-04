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
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.tab import MDTabsBase

class Tab(FloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
    #lock_swiping = True



class Info_tela(Screen):
    dados_clientes=[]
    popup_maps=None
    popup_editar=None
    data = {
        'point-of-sale': 'Vendas',
        'briefcase': 'Visitas'}

    def on_pre_enter(self):
        print('Entrando em Info_tela')
        app = MDApp.get_running_app()
        self.dados_clientes = app.dados_clientes
        app.registrar_tela()
        Window.bind(on_keyboard=app.voltar)
        #self.ids.info_tab.ids.scroll.scroll_y = 1

    def apagar_infos(self):
        print('Apagando infos da Info_tela')
        self.ids.info_tab.ids.codigo.text = ''
        self.ids.info_tab.ids.nome_fantasia.text = ''
        self.ids.info_tab.ids.endereco.text = ''
        self.ids.info_tab.ids.numero.text = ''
        self.ids.info_tab.ids.bairro.text = ''
        self.ids.info_tab.ids.telefone_fixo.text = ''
        self.ids.info_tab.ids.perfil_cliente.text = ''
        self.ids.info_tab.ids.nome_1.text = ''
        self.ids.info_tab.ids.telefone_1.text = ''
        self.ids.info_tab.ids.tipo_1.text = ''
        self.ids.info_tab.ids.nome_2.text = ''
        self.ids.info_tab.ids.telefone_2.text = ''
        self.ids.info_tab.ids.tipo_2.text = ''
        self.ids.info_tab.ids.nome_3.text = ''
        self.ids.info_tab.ids.telefone_3.text = ''
        self.ids.info_tab.ids.tipo_3.text = ''
        self.ids.info_tab.ids.banho.active = False
        self.ids.info_tab.ids.tosa.active = False
        self.ids.info_tab.ids.pet_shop.active = False
        self.ids.info_tab.ids.clinica.active = False
        self.ids.info_tab.ids.razao_social.text = ''
        self.ids.info_tab.ids.cnpj.text = ''
        self.ids.info_tab.ids.cep.text = ''
        self.ids.info_tab.ids.therapet.active = False
        self.ids.info_tab.ids.tesoura.active = False
        self.ids.info_tab.ids.tap_higienico.active = False
    
    def adicionar_infos(self,root):
        dados=[]
        print('Adicionando infos a Info_tela')
        if str(type(root)) == "<class 'kivy.weakproxy.WeakProxy'>" or str(root) == "<Screen name='Editar_tela'>":
            codigo = str(root.ids.codigo.text)
            dados=''
            print('Adicionando informações do cliente:', codigo)
            for cliente in self.dados_clientes:
                if codigo == str(cliente['codigo']):
                    dados = cliente
        else:
            lat = str(root)
            dados=''
            print('Adicionando informações do cliente na latitude:', lat)
            for cliente in self.dados_clientes:
                if lat == str(cliente['lat']):
                    dados = cliente
                    print('Cliente:', dados['nome_fantasia'])
           
        self.ids.info_tab.ids.codigo.text        = str(dados['codigo'])
        self.ids.info_tab.ids.nome_fantasia.text = str(dados['nome_fantasia'])
        self.ids.info_tab.ids.endereco.text      = str(dados['endereco'])
        self.ids.info_tab.ids.numero.text        = str(dados['numero'])
        self.ids.info_tab.ids.bairro.text        = str(dados['bairro'])
        self.ids.info_tab.ids.telefone_fixo.text = str(dados['telefone_fixo'])
        self.ids.info_tab.ids.perfil_cliente.text= str(dados['perfil_cliente'])
        self.ids.info_tab.ids.nome_1.text        = str(dados['nome_1'])
        self.ids.info_tab.ids.telefone_1.text    = str(dados['telefone_1'])
        self.ids.info_tab.ids.tipo_1.text        = str(dados['tipo_1'])
        self.ids.info_tab.ids.nome_2.text        = str(dados['nome_2'])
        self.ids.info_tab.ids.telefone_2.text    = str(dados['telefone_2'])
        self.ids.info_tab.ids.tipo_2.text        = str(dados['tipo_2'])
        self.ids.info_tab.ids.nome_3.text        = str(dados['nome_3'])
        self.ids.info_tab.ids.telefone_3.text    = str(dados['telefone_3'])
        self.ids.info_tab.ids.tipo_3.text        = str(dados['tipo_3'])
        self.ids.info_tab.ids.razao_social.text  = str(dados['razao_social'])
        self.ids.info_tab.ids.cnpj.text          = str(dados['cnpj'])
        self.ids.info_tab.ids.cep.text           = str(dados['cep'])

        x = (lambda a: 'Sim' if a == 'True' else '')

        self.ids.info_tab.ids.therapet.text    = x(str(dados['therapet']))
        self.ids.info_tab.ids.tesoura.text     = x(str(dados['tesoura']))
        self.ids.info_tab.ids.tap_higienico.text = x(str(dados['tap_higienico']))
        self.ids.info_tab.ids.banho.text       = x(str(dados['banho']))
        self.ids.info_tab.ids.tosa.text        = x(str(dados['tosa']))
        self.ids.info_tab.ids.pet_shop.text    = x(str(dados['pet_shop']))
        self.ids.info_tab.ids.clinica.text     = x(str(dados['clinica']))

    def abrir_popup_maps(self):    
        if not self.popup_maps:
            self.popup_maps = MDDialog( size_hint = [0.8,0.8],
                text="Deseja ir para rotas no Maps?",
                buttons=[
                    MDRaisedButton(
                        text="Sim", text_color=MDApp.get_running_app().theme_cls.primary_color, on_release = self.abrir_maps
                    ),
                    MDFlatButton(
                        text="Não", text_color=MDApp.get_running_app().theme_cls.primary_color, on_release = self.fechar_popup_maps
                    )
                ],
            )
        self.popup_maps.open()
    
    def abrir_maps(self,*args):
        import webbrowser
        print('Abrindo Google Maps')
        endereco = self.ids.info_tab.ids.endereco.text
        numero = self.ids.info_tab.ids.numero.text
        bairro = self.ids.info_tab.ids.bairro.text
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

    def fechar_popup_maps(self,*args):
        self.popup_maps.dismiss()

    def ir_para_mapa(self):
        for cliente in self.dados_clientes:
            if str(cliente['codigo']) == str(self.ids.info_tab.ids.codigo.text):
                dados = cliente
        try:
            lat,lon = float(dados['lat']), float(dados['lon'])
            app = MDApp.get_running_app()
            mapa_tela = app.root.get_screen('Mapa_tela')
            mapa_tela.ids.mapa.center_on(lat,lon)
            mapa_tela.ids.mapa.zoom = 16
            print('Indo para Mapa_tela centralizado em:', self.ids.info_tab.ids.nome_fantasia.text)
            app.root.transition.direction = 'right'
            app.root.current = 'Mapa_tela'
        except:
            pass

    def editar(self):
        if not self.popup_editar:
            app = MDApp.get_running_app()
            self.popup_editar = MDDialog( size_hint = [0.8,0.8],
                text="Deseja editar as informações desse cliente?",
                buttons=[
                    MDRaisedButton(
                        text="Sim", text_color=app.theme_cls.accent_dark, on_release = self.ir_para_Editar_tela
                    ),
                    MDFlatButton(
                        text="Não", text_color=app.theme_cls.primary_color, on_release = self.fechar_popup_editar
                    )
                ],
            )
        self.popup_editar.open()
    
    def ir_para_Editar_tela(self,root,*args):
        app = MDApp.get_running_app()
        app.root.transition.direction = 'left'
        app.root.current = 'Editar_tela'
        root = app.root.get_screen('Info_tela')
        app.root.get_screen('Editar_tela').adicionar_infos(root)
        self.fechar_popup_editar()
    
    def fechar_popup_editar(self,*args):
        self.popup_editar.dismiss()



    def callback(self, instance):
        if instance.icon == 'briefcase':
            app = MDApp.get_running_app()
            app.popup_leituradados.open()
            Clock.schedule_once(self.abrir_visitas,0.1)
        if instance.icon == 'point-of-sale':
            pass
           
    def abrir_visitas(self,*args):
        print('Executando abrir_visitas em main')
        app = MDApp.get_running_app()
        info_tela = app.root.get_screen('Info_tela')
        visitas_tela = app.root.get_screen('Visitas_tela')
        visitas_tela.ids.buscar.text = info_tela.ids.nome_fantasia.text
        visitas_tela.ids.data.text = ''
        visitas_tela.mostrar_popup()
        app.root.transition.direction = 'left'
        app.root.current = 'Visitas_tela'
        

