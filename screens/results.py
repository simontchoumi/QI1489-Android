from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard

KV = '''
<ResultsScreen>:
    name: 'results'
    canvas.before:
        Color:
            rgba: 0.039, 0.055, 0.153, 1
        Rectangle:
            pos: self.pos
            size: self.size

    ScrollView:
        MDBoxLayout:
            orientation: 'vertical'
            spacing: dp(16)
            padding: dp(20)
            adaptive_height: True

            Widget:
                size_hint_y: None
                height: dp(20)

            MDLabel:
                id: result_title
                text: 'Game Over!'
                halign: 'center'
                font_style: 'H4'
                theme_text_color: 'Custom'
                text_color: 0.424, 0.388, 1, 1
                size_hint_y: None
                height: dp(50)

            # Score card
            MDCard:
                orientation: 'vertical'
                padding: dp(24)
                spacing: dp(12)
                size_hint_y: None
                height: dp(200)
                md_bg_color: 0.082, 0.094, 0.204, 1
                radius: [dp(16)]

                MDLabel:
                    id: score_big
                    text: '0'
                    halign: 'center'
                    font_style: 'H2'
                    theme_text_color: 'Custom'
                    text_color: 1, 0.718, 0.012, 1

                MDLabel:
                    id: correct_label
                    text: '0 / 0 correct'
                    halign: 'center'
                    font_style: 'H6'
                    theme_text_color: 'Custom'
                    text_color: 1, 1, 1, 1

                MDLabel:
                    id: percent_label
                    text: '0%'
                    halign: 'center'
                    font_style: 'Subtitle1'
                    theme_text_color: 'Custom'
                    text_color: 0.024, 0.839, 0.627, 1

                MDLabel:
                    id: time_label
                    text: 'Time: 0s'
                    halign: 'center'
                    font_style: 'Caption'
                    theme_text_color: 'Custom'
                    text_color: 0.533, 0.569, 0.69, 1

            # Disclaimer card
            MDCard:
                id: disclaimer_card
                orientation: 'vertical'
                padding: dp(16)
                size_hint_y: None
                height: dp(80)
                md_bg_color: 0.082, 0.094, 0.204, 0.8
                radius: [dp(12)]

                MDLabel:
                    id: disclaimer_text
                    text: ''
                    halign: 'center'
                    theme_text_color: 'Custom'
                    text_color: 0.533, 0.569, 0.69, 1
                    font_style: 'Caption'

            # Buttons
            MDRaisedButton:
                text: 'Play Again'
                md_bg_color: 0.424, 0.388, 1, 1
                size_hint_x: 1
                height: dp(48)
                size_hint_y: None
                on_release: root.play_again()

            MDRaisedButton:
                text: 'Leaderboard'
                md_bg_color: 0.024, 0.839, 0.627, 0.9
                size_hint_x: 1
                height: dp(48)
                size_hint_y: None
                on_release: root.go_leaderboard()

            MDFlatButton:
                text: 'Main Menu'
                theme_text_color: 'Custom'
                text_color: 0.533, 0.569, 0.69, 1
                size_hint_x: 1
                height: dp(44)
                size_hint_y: None
                on_release: root.go_menu()

            Widget:
                size_hint_y: None
                height: dp(20)
'''

Builder.load_string(KV)


class ResultsScreen(MDScreen):
    def on_enter(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        lang = app.lang
        score_data = app.last_score or {}

        score = score_data.get('score', 0)
        correct = score_data.get('correct', 0)
        total = score_data.get('total', 0)
        time_played = score_data.get('time_played', 0)
        pct = round((correct / total * 100) if total > 0 else 0)

        self.ids.score_big.text = str(score)
        self.ids.correct_label.text = f'{correct} / {total} correct'
        self.ids.percent_label.text = f'{pct}%'
        self.ids.time_label.text = f'Time: {time_played}s'

        # Color score by performance
        if pct >= 80:
            self.ids.score_big.text_color = (0.024, 0.839, 0.627, 1)
        elif pct >= 50:
            self.ids.score_big.text_color = (1, 0.718, 0.012, 1)
        else:
            self.ids.score_big.text_color = (0.937, 0.278, 0.435, 1)

        if lang == 'fr':
            self.ids.result_title.text = 'Partie terminee!'
            self.ids.correct_label.text = f'{correct} / {total} correctes'

        # Disclaimer
        disc = app.db.get_disclaimer()
        disc_text = disc.get('text_fr', '') if lang == 'fr' else disc.get('text_en', '')
        self.ids.disclaimer_text.text = disc_text

    def play_again(self):
        self.manager.current = 'play'

    def go_leaderboard(self):
        self.manager.current = 'leaderboard'

    def go_menu(self):
        self.manager.current = 'menu'
