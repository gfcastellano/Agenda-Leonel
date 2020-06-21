from kivymd.app import MDApp
from mapview import MapMarkerPopup

class Marcador(MapMarkerPopup):
    def on_release(self):
        app = MDApp.get_running_app()
        app.root.transition.direction = 'left'
        app.root.current = 'Info_tela'
        app.root.get_screen('Info_tela').adicionar_infos(self.lat)