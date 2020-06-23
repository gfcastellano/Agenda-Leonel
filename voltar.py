from kivy.core.window import Window
from kivymd.app import MDApp


class Voltar():
    window=None
    key=None
    def registrar_tela(self):        
        app = MDApp.get_running_app()
        gerenciador = app.root
        app.telas.append(str(gerenciador.current_screen)[14:-2])

    def voltar(self,window,key,*args):
        if key ==27: #27 = esc
            app = MDApp.get_running_app()
            try:
                ultima_tela = str(app.telas[-2])
            except IndexError:
                ultima_tela = str(app.telas[-1])
            tela_atual = str(app.telas[-1])

            print('----------------------------------------------------------------------------------Ultima tela:',ultima_tela)
            if ultima_tela == 'Info_tela':
                print('[voltar] if')
                app.root.transition.direction = 'left'                
                app.root.current = str(app.telas[-2])
            else:
                print('[voltar] elif')
                app.root.transition.direction = 'left'
                app.root.current = str(app.telas[-2])
                app.root.transition.direction = 'right'
            # Aqui faz com que o voltar não fique sempre pulando entre as duas ultimas telas
            try:  
                if app.telas[-1] == app.telas[-3]:
                    app.telas = app.telas[:-2]
            except IndexError:
                app.telas = app.telas[:-1]
        return True

        if key == 113: # 113 = q
            app = MDApp.get_running_app()
            print(app.telas)

    