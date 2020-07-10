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
from kivymd.uix.tab import MDTabsBase
from kivy.uix.floatlayout import FloatLayout


class Tab(FloatLayout, MDTabsBase):
    pass


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
        self.ids.info_tab.ids.scroll_info.scroll_y = 1

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

        #Identificar cliente
        if str(type(root)) == "<class 'kivy.weakproxy.WeakProxy'>" or str(root) == "<Screen name='Editar_tela'>":
            codigo = str(root.ids.codigo.text)
            dados=''
            print('Adicionando informações do cliente:', codigo)
            for cliente in self.dados_clientes:
                if codigo == str(cliente['codigo']):
                    dados = cliente
        else:
            lat = str(root)
            print('Tamanho de root:',len(str(root)))
            if len(str(root)) > 11:
                for i in range(0,20):
                    print('tamanho i:',i)
                    retirar = len(str(root)) - 11 - i
                    print('tamanho retirar:',retirar)
                    lat = str(root)[:-retirar]
                    print('Tamanho de lat:',len(lat))
                    dados=''
                    print('Adicionando informações do cliente na latitude:', lat)
                    for cliente in self.dados_clientes:
                        if str(cliente['lat']) == lat:
                            dados = cliente
                            print('Cliente:', dados['nome_fantasia'])
                    if dados == '':
                        print('Não houve match nos dados')
                        continue
                    else:
                        break
            else:
                dados=''
                print('Adicionando informações do cliente na latitude:', lat)
                for cliente in self.dados_clientes:
                    if str(cliente['lat']) == lat:
                        dados = cliente
                        print('Cliente:', dados['nome_fantasia'])

        #Preencher informações no info_tab

        info_tab = self.ids.info_tab  
        info_tab.ids.codigo.text        = str(dados['codigo'])
        info_tab.ids.nome_fantasia.text = str(dados['nome_fantasia'])
        info_tab.ids.endereco.text      = str(dados['endereco'])
        info_tab.ids.numero.text        = str(dados['numero'])
        info_tab.ids.bairro.text        = str(dados['bairro'])
        info_tab.ids.telefone_fixo.text = str(dados['telefone_fixo'])
        info_tab.ids.perfil_cliente.text= str(dados['perfil_cliente'])
        info_tab.ids.nome_1.text        = str(dados['nome_1'])
        info_tab.ids.telefone_1.text    = str(dados['telefone_1'])
        info_tab.ids.tipo_1.text        = str(dados['tipo_1'])
        info_tab.ids.nome_2.text        = str(dados['nome_2'])
        info_tab.ids.telefone_2.text    = str(dados['telefone_2'])
        info_tab.ids.tipo_2.text        = str(dados['tipo_2'])
        info_tab.ids.nome_3.text        = str(dados['nome_3'])
        info_tab.ids.telefone_3.text    = str(dados['telefone_3'])
        info_tab.ids.tipo_3.text        = str(dados['tipo_3'])
        info_tab.ids.razao_social.text  = str(dados['razao_social'])
        info_tab.ids.cnpj.text          = str(dados['cnpj'])
        info_tab.ids.cep.text           = str(dados['cep'])

        x = (lambda a: 'Sim' if a == 'True' else '')

        info_tab.ids.therapet.text    = x(str(dados['therapet']))
        info_tab.ids.tesoura.text     = x(str(dados['tesoura']))
        info_tab.ids.tap_higienico.text = x(str(dados['tap_higienico']))
        info_tab.ids.banho.text       = x(str(dados['banho']))
        info_tab.ids.tosa.text        = x(str(dados['tosa']))
        info_tab.ids.pet_shop.text    = x(str(dados['pet_shop']))
        info_tab.ids.clinica.text     = x(str(dados['clinica']))

        #Adidionando informações no visitas_tab
        self.ids.visitas_tab.ids.buscar.text = self.ids.info_tab.ids.nome_fantasia.text
        visitas_tela = MDApp.get_running_app().root.get_screen('Visitas_tela')
        visitas_tela.ids.buscar.text = self.ids.info_tab.ids.nome_fantasia.text
        visitas_tela.buscar()

        self.ids.visitas_tab.ids.scroll_visitas.children = visitas_tela.ids.scroll.children




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

    def fechar_popup_maps(self,*args):
        self.popup_maps.dismiss()

    def ir_para_mapa(self):
        for cliente in self.dados_clientes:
            if str(cliente['codigo']) == str(self.ids.codigo.text):
                dados = cliente
        try:
            lat,lon = float(dados['lat']), float(dados['lon'])
            app = MDApp.get_running_app()
            mapa_tela = app.root.get_screen('Mapa_tela')
            mapa_tela.ids.mapa.center_on(lat,lon)
            mapa_tela.ids.mapa.zoom = 16
            print('Indo para Mapa_tela centralizado em:', self.ids.nome_fantasia.text)
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
        print('Executando abrir_visitas em info_tela')
        app = MDApp.get_running_app()
        info_tela = app.root.get_screen('Info_tela')
        visitas_tela = app.root.get_screen('Visitas_tela')
        app.root.transition.direction = 'left'
        app.root.current = 'Visitas_tela'
        visitas_tela.ids.buscar.text = info_tela.ids.nome_fantasia.text
        visitas_tela.ids.data.text = ''  
        visitas_tela.mostrar_popup()
        

