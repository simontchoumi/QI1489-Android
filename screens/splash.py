from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.label import MDLabel

KV = '''
<SplashScreen>:
    name: 'splash'
    canvas.before:
        Color:
            rgba: 0.039, 0.055, 0.153, 1
        Rectangle:
            pos: self.pos
            size: self.size

    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(16)
        padding: dp(40)
        pos_hint: {'center_x': .5, 'center_y': .5}
        size_hint: None, None
        size: dp(300), dp(260)

        MDLabel:
            text: 'QI'
            halign: 'center'
            font_style: 'H1'
            theme_text_color: 'Custom'
            text_color: 0.424, 0.388, 1, 1
            size_hint_y: None
            height: dp(90)

        MDLabel:
            text: '1489'
            halign: 'center'
            font_style: 'H2'
            theme_text_color: 'Custom'
            text_color: 1, 0.718, 0.012, 1
            size_hint_y: None
            height: dp(60)

        MDLabel:
            text: 'World Knowledge Quiz'
            halign: 'center'
            font_style: 'Subtitle1'
            theme_text_color: 'Custom'
            text_color: 0.533, 0.569, 0.69, 1

        Widget:
            size_hint_y: None
            height: dp(20)

        MDSpinner:
            id: spinner
            size_hint: None, None
            size: dp(40), dp(40)
            pos_hint: {'center_x': .5}
            color: 0.424, 0.388, 1, 1

        MDLabel:
            text: 'Loading...'
            halign: 'center'
            font_style: 'Caption'
            theme_text_color: 'Custom'
            text_color: 0.533, 0.569, 0.69, 1
'''

Builder.load_string(KV)


class SplashScreen(MDScreen):
    def on_enter(self):
        Clock.schedule_once(self._go_to_menu, 2.0)

    def _go_to_menu(self, dt):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        app.db.initialize()
        self.manager.current = 'menu'
