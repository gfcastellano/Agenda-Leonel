from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window



class Menu(Screen):

    
    def on_enter(self):
        print('Entrando em Menu_tela')
        app = MDApp.get_running_app()
        print('Carregamento de clientes automático ao voltar para Menu_tela')
        app.carregar_clientes()
        app.registrar_tela()        
        try:  # Devemos colocar como try except pois na inicialização daria erro
            gerenciador.transition.direction = 'left'
        except:
            pass  
        Window.bind(on_keyboard=app.voltar)
        


