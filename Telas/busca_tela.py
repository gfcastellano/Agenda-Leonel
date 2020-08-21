from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window


class Busca_tela(Screen):
    def on_pre_enter(self):
        print('Entrando em Busca_tela')
        app = MDApp.get_running_app()
        app.registrar_tela()
        Window.bind(on_keyboard=app.voltar)
        self.ids.scroll.scroll_y = 1
        self.dados_clientes = app.dados_clientes

    def apagar_texto(self,id):
        field = MDApp.get_running_app().root.get_screen('Busca_tela').ids
        field[id].text = ''

    def mostrar_popup(self):
        MDApp.get_running_app().popup_leituradados.open()
        #print('[Busca_tela.mostrar_popup()] Tamanho de dados_clientes:',len(self.dados_clientes))
        Clock.schedule_once(self.busca_avancada,0.1)

    def busca_avancada(self,*args):
        print('Executando busca avançada')
        field = MDApp.get_running_app().root.get_screen('Busca_tela').ids
        dicionario = {'codigo':  field['codigo'].text,
        'nome_fantasia' : field['nome_fantasia'].text,
        'endereco'      : field['endereco'].text,
        'bairro'        : field['bairro'].text,
        'telefone'      : field['telefone'].text,
        'contato'       : field['contato'].text,
        'perfil'        : field['perfil'].text,
        'banho'         : field['banho'].active,
        'tosa'          : field['tosa'].active,
        'pet_shop'      : field['pet_shop'].active,
        'clinica'       : field['clinica'].active,
        'razao_social'  : field['razao_social'].text,
        'cnpj'          : field['cnpj'].text,
        'cep'           : field['cep'].text,
        'therapet'      : field['therapet'].active,
        'tesoura'       : field['tesoura'].active,
        'tap_higienico' : field['tap_higienico'].active}


        retirar=[]
        for item in dicionario:
            try:
                if len(dicionario[item]) == 0: 
                    retirar.append(item)
            except TypeError:
                if dicionario[item] == False:
                    retirar.append(item)
        for item in retirar:
            del dicionario[item]

        print('Buscando por:')
        for key, value in dicionario.items():            
            print('\t',key,' --> ',value)

        retirar=[]
        match = self.dados_clientes.copy()
        for item in dicionario:
            print('Buscando por item:', item)
            print('Clientes na busca:', len(match))
            for cliente in match:                
                if item == 'telefone':
                    if (str(dicionario[item]).lower() not in str(cliente['telefone_fixo']).lower()) and\
                       (str(dicionario[item]).lower() not in str(cliente['telefone_1']).lower()) and \
                       (str(dicionario[item]).lower() not in str(cliente['telefone_2']).lower()) and \
                       (str(dicionario[item]).lower() not in str(cliente['telefone_3']).lower()):
                        retirar.append(cliente)
                elif item == 'contato':
                    if (str(dicionario[item]).lower() not in str(cliente['nome_1']).lower()) and \
                       (str(dicionario[item]).lower() not in str(cliente['nome_2']).lower()) and \
                       (str(dicionario[item]).lower() not in str(cliente['nome_3']).lower()):
                        retirar.append(cliente)
                elif item == 'perfil':
                    if (str(dicionario[item]).lower() not in str(cliente['tipo_1']).lower()) and \
                       (str(dicionario[item]).lower() not in str(cliente['tipo_2']).lower()) and \
                       (str(dicionario[item]).lower() not in str(cliente['tipo_3']).lower()):
                        retirar.append(cliente)
                else:
                    #print(str(dicionario[item]).lower(), '         |         ',str(cliente[item]).lower(), '         |         ',str(cliente['nome_fantasia']))
                    if str(dicionario[item]).lower() != str(cliente[item]).lower():
                        retirar.append(cliente)
                    else:
                        pass
                        #print(cliente['nome_fantasia'],' | ',cliente[item])
                        
            print('Tamanho de retirar:', len(retirar))
            for x in retirar:
                match.remove(x)
            retirar=[]

        clientes_tela = MDApp.get_running_app().root.get_screen('Clientes_tela')
        clientes_tela.apagar_clientes()
        clientes_tela.adicionar_clientes(match)
        clientes_tela.apagar_texto()
        #MDApp.get_running_app().carregar_clientes() #Não entendo pq dá um erro se não executar isso.
        # Ele usa o match que é passado na chamada da função acima e instaura o Clientes_tela.dados_clientes como match.
        MDApp.get_running_app().root.transition.direction = 'left'
        MDApp.get_running_app().root.current = 'Clientes_tela'
        clientes_tela.fechar_popup()
