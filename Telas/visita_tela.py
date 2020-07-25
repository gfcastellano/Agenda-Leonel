from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivymd.uix.picker import MDDatePicker
from datetime import date


class Visita_tela(Screen):
    def on_pre_enter(self):
        print('Entrando em Visita_tela')
        app = MDApp.get_running_app()
        app.registrar_tela()
        Window.bind(on_keyboard=app.voltar)
        
        self.dados_clientes = app.dados_clientes
        self.dados_visitas  = app.dados_visitas
        data = date.today()
        self.primeiro_dia = str(data.day) if len(str(data.day)) > 1 else '0'+str(data.day)
        self.primeiro_mes = str(data.month) if len(str(data.month)) > 1 else '0'+str(data.month)
        self.primeiro_ano = str(data.year)
        self.ids.data.text = self.primeiro_dia + '/' + self.primeiro_mes + '/' + self.primeiro_ano


    def abrir_popup_data(self):
        primeiro_calendario = MDDatePicker(callback = self.marcar_data_visita)
        primeiro_calendario.open()

    def marcar_data_visita(self, data):
        self.primeiro_dia = str(data.day) if len(str(data.day)) > 1 else '0'+str(data.day)
        self.primeiro_mes = str(data.month) if len(str(data.month)) > 1 else '0'+str(data.month)
        self.primeiro_ano = str(data.year)
        self.ids.data.text = self.primeiro_dia + '/' + self.primeiro_mes + '/' + self.primeiro_ano

    def abrir_popup_data_lembrete(self):
        primeiro_calendario = MDDatePicker(callback = self.marcar_data_lembrete)
        primeiro_calendario.open()

    def marcar_data_lembrete(self, data):
        self.primeiro_dia = str(data.day) if len(str(data.day)) > 1 else '0'+str(data.day)
        self.primeiro_mes = str(data.month) if len(str(data.month)) > 1 else '0'+str(data.month)
        self.primeiro_ano = str(data.year)
        self.ids.data_lembrete.text = self.primeiro_dia + '/' + self.primeiro_mes + '/' + self.primeiro_ano