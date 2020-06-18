from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout


class Busca_tela(Screen):
    def apagar_texto(self,id):
        field = MDApp.get_running_app().root.get_screen('Busca_tela').ids
        field[id].text = ''

