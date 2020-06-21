from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window



class Menu(Screen):

    def on_enter(self):
        print('Entrando em Menu_tela')
        app = MDApp.get_running_app()
        gerenciador = app.root
        try:
            app.telas.append(str(gerenciador.current_screen)[14:-2])
        except:
            pass
        try: 
            gerenciador.transition.direction = 'left'
        except:
            pass  
        Window.bind(on_keyboard=self.voltar)

        
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
