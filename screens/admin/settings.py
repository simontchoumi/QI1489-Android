from kivy.lang import Builder
from kivy.metrics import dp
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard

KV = '''
<AdminSettingsScreen>:
    name: 'admin_settings'
    canvas.before:
        Color:
            rgba: 0.039, 0.055, 0.153, 1
        Rectangle:
            pos: self.pos
            size: self.size

    MDBoxLayout:
        orientation: 'vertical'

        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(56)
            padding: dp(8), dp(4)
            canvas.before:
                Color:
                    rgba: 0.055, 0.071, 0.184, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            MDIconButton:
                icon: 'arrow-left'
                theme_icon_color: 'Custom'
                icon_color: 1, 1, 1, 1
                on_release: root.go_back()

            MDLabel:
                text: 'Settings'
                font_style: 'H6'
                theme_text_color: 'Custom'
                text_color: 1, 1, 1, 1

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(16)
                padding: dp(16)
                adaptive_height: True

                # Game settings
                MDCard:
                    orientation: 'vertical'
                    padding: dp(16)
                    spacing: dp(12)
                    size_hint_y: None
                    height: dp(230)
                    md_bg_color: 0.082, 0.094, 0.204, 1
                    radius: [dp(14)]

                    MDLabel:
                        text: 'Game Settings'
                        font_style: 'H6'
                        theme_text_color: 'Custom'
                        text_color: 0.424, 0.388, 1, 1
                        size_hint_y: None
                        height: dp(30)

                    MDLabel:
                        text: 'Questions per session'
                        font_style: 'Subtitle2'
                        theme_text_color: 'Custom'
                        text_color: 1, 1, 1, 1
                        size_hint_y: None
                        height: dp(24)

                    MDBoxLayout:
                        orientation: 'horizontal'
                        spacing: dp(8)
                        size_hint_y: None
                        height: dp(44)

                        MDIconButton:
                            icon: 'minus'
                            theme_icon_color: 'Custom'
                            icon_color: 0.937, 0.278, 0.435, 1
                            size_hint_x: None
                            width: dp(44)
                            on_release: root.adjust_questions(-1)

                        MDTextField:
                            id: questions_field
                            hint_text: '10'
                            mode: 'rectangle'
                            input_filter: 'int'
                            size_hint_y: None
                            height: dp(44)

                        MDIconButton:
                            icon: 'plus'
                            theme_icon_color: 'Custom'
                            icon_color: 0.024, 0.839, 0.627, 1
                            size_hint_x: None
                            width: dp(44)
                            on_release: root.adjust_questions(1)

                    MDLabel:
                        text: 'Seconds per question'
                        font_style: 'Subtitle2'
                        theme_text_color: 'Custom'
                        text_color: 1, 1, 1, 1
                        size_hint_y: None
                        height: dp(24)

                    MDBoxLayout:
                        orientation: 'horizontal'
                        spacing: dp(8)
                        size_hint_y: None
                        height: dp(44)

                        MDIconButton:
                            icon: 'minus'
                            theme_icon_color: 'Custom'
                            icon_color: 0.937, 0.278, 0.435, 1
                            size_hint_x: None
                            width: dp(44)
                            on_release: root.adjust_time(-5)

                        MDTextField:
                            id: time_field
                            hint_text: '15'
                            mode: 'rectangle'
                            input_filter: 'int'
                            size_hint_y: None
                            height: dp(44)

                        MDIconButton:
                            icon: 'plus'
                            theme_icon_color: 'Custom'
                            icon_color: 0.024, 0.839, 0.627, 1
                            size_hint_x: None
                            width: dp(44)
                            on_release: root.adjust_time(5)

                MDRaisedButton:
                    text: 'Save Game Settings'
                    md_bg_color: 0.424, 0.388, 1, 1
                    size_hint_x: 1
                    height: dp(48)
                    size_hint_y: None
                    on_release: root.save_game_settings()

                # Disclaimer
                MDCard:
                    orientation: 'vertical'
                    padding: dp(16)
                    spacing: dp(10)
                    size_hint_y: None
                    height: dp(270)
                    md_bg_color: 0.082, 0.094, 0.204, 1
                    radius: [dp(14)]

                    MDLabel:
                        text: 'End-of-Game Disclaimer'
                        font_style: 'H6'
                        theme_text_color: 'Custom'
                        text_color: 0.024, 0.839, 0.627, 1
                        size_hint_y: None
                        height: dp(30)

                    MDTextField:
                        id: disclaimer_en
                        hint_text: 'Disclaimer (English)'
                        mode: 'rectangle'
                        multiline: True
                        size_hint_y: None
                        height: dp(90)

                    MDTextField:
                        id: disclaimer_fr
                        hint_text: 'Disclaimer (French)'
                        mode: 'rectangle'
                        multiline: True
                        size_hint_y: None
                        height: dp(90)

                MDRaisedButton:
                    text: 'Save Disclaimer'
                    md_bg_color: 0.024, 0.839, 0.627, 0.9
                    size_hint_x: 1
                    height: dp(48)
                    size_hint_y: None
                    on_release: root.save_disclaimer()

                # Update DB
                MDCard:
                    orientation: 'vertical'
                    padding: dp(16)
                    spacing: dp(10)
                    size_hint_y: None
                    height: dp(160)
                    md_bg_color: 0.082, 0.094, 0.204, 1
                    radius: [dp(14)]

                    MDLabel:
                        text: 'Update Question Database'
                        font_style: 'H6'
                        theme_text_color: 'Custom'
                        text_color: 1, 0.718, 0.012, 1
                        size_hint_y: None
                        height: dp(30)

                    MDLabel:
                        text: 'Fetches latest country data from internet and reloads all static questions.'
                        font_style: 'Caption'
                        theme_text_color: 'Custom'
                        text_color: 0.533, 0.569, 0.69, 1
                        size_hint_y: None
                        height: dp(40)

                    MDRaisedButton:
                        id: update_btn
                        text: 'Update from Internet'
                        md_bg_color: 1, 0.718, 0.012, 0.9
                        size_hint_x: 1
                        height: dp(48)
                        size_hint_y: None
                        on_release: root.update_database()

                    MDLabel:
                        id: update_status
                        text: ''
                        font_style: 'Caption'
                        theme_text_color: 'Custom'
                        text_color: 0.024, 0.839, 0.627, 1
                        halign: 'center'
                        size_hint_y: None
                        height: dp(24)

                # App Info
                MDCard:
                    orientation: 'vertical'
                    padding: dp(16)
                    spacing: dp(4)
                    size_hint_y: None
                    height: dp(130)
                    md_bg_color: 0.082, 0.094, 0.204, 1
                    radius: [dp(14)]

                    MDLabel:
                        text: 'App Info'
                        font_style: 'H6'
                        theme_text_color: 'Custom'
                        text_color: 1, 0.718, 0.012, 1
                        size_hint_y: None
                        height: dp(30)

                    MDLabel:
                        text: 'QI1489 — World Knowledge Quiz'
                        font_style: 'Subtitle2'
                        theme_text_color: 'Custom'
                        text_color: 1, 1, 1, 1

                    MDLabel:
                        text: 'Owner: Simon TCHOUMI NJANJOU'
                        font_style: 'Caption'
                        theme_text_color: 'Custom'
                        text_color: 0.533, 0.569, 0.69, 1

                    MDLabel:
                        text: 'Company: SMJx Game'
                        font_style: 'Caption'
                        theme_text_color: 'Custom'
                        text_color: 0.533, 0.569, 0.69, 1

                    MDLabel:
                        text: 'Donation: +237676262622'
                        font_style: 'Caption'
                        theme_text_color: 'Custom'
                        text_color: 1, 0.718, 0.012, 1

                Widget:
                    size_hint_y: None
                    height: dp(20)
'''

Builder.load_string(KV)


class AdminSettingsScreen(MDScreen):
    def on_enter(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        self.ids.questions_field.text = app.db.get_setting('questions_per_game', '10')
        self.ids.time_field.text = app.db.get_setting('question_time', '15')
        disc = app.db.get_disclaimer()
        self.ids.disclaimer_en.text = disc.get('text_en', '')
        self.ids.disclaimer_fr.text = disc.get('text_fr', '')
        self.ids.update_status.text = ''

    def adjust_questions(self, delta):
        try:
            val = int(self.ids.questions_field.text or '10') + delta
            val = max(3, min(50, val))
            self.ids.questions_field.text = str(val)
        except ValueError:
            self.ids.questions_field.text = '10'

    def adjust_time(self, delta):
        try:
            val = int(self.ids.time_field.text or '15') + delta
            val = max(5, min(60, val))
            self.ids.time_field.text = str(val)
        except ValueError:
            self.ids.time_field.text = '15'

    def save_game_settings(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        try:
            qpg = max(3, min(50, int(self.ids.questions_field.text or '10')))
            qt = max(5, min(60, int(self.ids.time_field.text or '15')))
            app.db.set_setting('questions_per_game', str(qpg))
            app.db.set_setting('question_time', str(qt))
            self.ids.questions_field.text = str(qpg)
            self.ids.time_field.text = str(qt)
            Snackbar(text=f'Saved: {qpg} questions, {qt}s per question.',
                     snackbar_x='10dp', snackbar_y='10dp', size_hint_x=0.9,
                     bg_color=(0.024, 0.839, 0.627, 1)).open()
        except ValueError:
            Snackbar(text='Invalid values.', snackbar_x='10dp', snackbar_y='10dp',
                     size_hint_x=0.9, bg_color=(0.937, 0.278, 0.435, 1)).open()

    def save_disclaimer(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        app.db.save_disclaimer(
            text_en=self.ids.disclaimer_en.text.strip(),
            text_fr=self.ids.disclaimer_fr.text.strip(),
        )
        Snackbar(text='Disclaimer saved.', snackbar_x='10dp', snackbar_y='10dp',
                 size_hint_x=0.9, bg_color=(0.024, 0.839, 0.627, 1)).open()

    def update_database(self):
        from threading import Thread
        self.ids.update_btn.disabled = True
        self.ids.update_status.text = 'Updating... please wait'

        def _run():
            from kivymd.app import MDApp
            from services.update_service import update_all_questions
            app = MDApp.get_running_app()
            try:
                result = update_all_questions(app.db)
                Clock.schedule_once(lambda dt: self._update_done(result), 0)
            except Exception as e:
                Clock.schedule_once(lambda dt, err=str(e): self._update_error(err), 0)

        Thread(target=_run, daemon=True).start()

    def _update_done(self, result):
        self.ids.update_btn.disabled = False
        msg = f"Done: {result['added']} added, {result['updated']} updated."
        self.ids.update_status.text = msg
        Snackbar(text=msg, snackbar_x='10dp', snackbar_y='10dp',
                 size_hint_x=0.9, bg_color=(0.024, 0.839, 0.627, 1)).open()

    def _update_error(self, err):
        self.ids.update_btn.disabled = False
        self.ids.update_status.text = f'Error: {err}'
        Snackbar(text=f'Update failed: {err[:50]}', snackbar_x='10dp', snackbar_y='10dp',
                 size_hint_x=0.9, bg_color=(0.937, 0.278, 0.435, 1)).open()

    def go_back(self):
        self.manager.current = 'admin_dashboard'
