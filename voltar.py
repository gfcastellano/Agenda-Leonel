from kivy.core.window import Window
from kivymd.app import MDApp


class Voltar():
    def registrar_tela(self):        
        app = MDApp.get_running_app()
        gerenciador = app.root
        app.telas.append(str(gerenciador.current_screen)[14:-2])
        Window.bind(on_keyboard=Voltar.voltar)

    def voltar(self,window,key,*args):
        if key ==27:
            gerenciador = MDApp.get_running_app().root
            app = MDApp.get_running_app()
            gerenciador.current = str(app.telas[-2])
            return True
        if key == 113:
            app = MDApp.get_running_app()
            print(app.telas)

    