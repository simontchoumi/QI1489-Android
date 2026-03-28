from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard

KV = '''
<ProfileScreen>:
    name: 'profile'
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
                text: 'Profile'
                font_style: 'H6'
                theme_text_color: 'Custom'
                text_color: 1, 1, 1, 1

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(16)
                padding: dp(20)
                adaptive_height: True

                Widget:
                    size_hint_y: None
                    height: dp(20)

                # Avatar + name card
                MDCard:
                    orientation: 'vertical'
                    padding: dp(24)
                    spacing: dp(8)
                    size_hint_y: None
                    height: dp(180)
                    md_bg_color: 0.082, 0.094, 0.204, 1
                    radius: [dp(16)]

                    MDLabel:
                        id: avatar_icon
                        text: 'A'
                        halign: 'center'
                        font_style: 'H3'
                        theme_text_color: 'Custom'
                        text_color: 0.424, 0.388, 1, 1

                    MDLabel:
                        id: username_lbl
                        text: ''
                        halign: 'center'
                        font_style: 'H6'
                        theme_text_color: 'Custom'
                        text_color: 1, 1, 1, 1

                    MDLabel:
                        id: rank_lbl
                        text: ''
                        halign: 'center'
                        font_style: 'Subtitle2'
                        theme_text_color: 'Custom'
                        text_color: 1, 0.718, 0.012, 1

                    MDLabel:
                        id: email_lbl
                        text: ''
                        halign: 'center'
                        font_style: 'Caption'
                        theme_text_color: 'Custom'
                        text_color: 0.533, 0.569, 0.69, 1

                # Stats card
                MDCard:
                    orientation: 'horizontal'
                    padding: dp(16)
                    spacing: dp(0)
                    size_hint_y: None
                    height: dp(80)
                    md_bg_color: 0.082, 0.094, 0.204, 1
                    radius: [dp(12)]

                    MDBoxLayout:
                        orientation: 'vertical'
                        spacing: dp(4)

                        MDLabel:
                            id: games_lbl
                            text: '0'
                            halign: 'center'
                            font_style: 'H5'
                            theme_text_color: 'Custom'
                            text_color: 0.424, 0.388, 1, 1

                        MDLabel:
                            text: 'Games'
                            halign: 'center'
                            font_style: 'Caption'
                            theme_text_color: 'Custom'
                            text_color: 0.533, 0.569, 0.69, 1

                    MDBoxLayout:
                        orientation: 'vertical'
                        spacing: dp(4)

                        MDLabel:
                            id: score_lbl
                            text: '0'
                            halign: 'center'
                            font_style: 'H5'
                            theme_text_color: 'Custom'
                            text_color: 1, 0.718, 0.012, 1

                        MDLabel:
                            text: 'Total Score'
                            halign: 'center'
                            font_style: 'Caption'
                            theme_text_color: 'Custom'
                            text_color: 0.533, 0.569, 0.69, 1

                # Language toggle
                MDCard:
                    orientation: 'vertical'
                    padding: dp(16)
                    spacing: dp(8)
                    size_hint_y: None
                    height: dp(80)
                    md_bg_color: 0.082, 0.094, 0.204, 1
                    radius: [dp(12)]

                    MDLabel:
                        text: 'Language'
                        font_style: 'Subtitle2'
                        theme_text_color: 'Custom'
                        text_color: 1, 1, 1, 1

                    MDBoxLayout:
                        orientation: 'horizontal'
                        spacing: dp(12)

                        MDRaisedButton:
                            id: btn_en
                            text: 'English'
                            size_hint_x: 1
                            height: dp(36)
                            size_hint_y: None
                            on_release: root.set_lang('en')

                        MDRaisedButton:
                            id: btn_fr
                            text: 'Francais'
                            size_hint_x: 1
                            height: dp(36)
                            size_hint_y: None
                            on_release: root.set_lang('fr')

                # Admin button (shown only for admins)
                MDRaisedButton:
                    id: admin_btn
                    text: 'Admin Panel'
                    md_bg_color: 1, 0.718, 0.012, 1
                    size_hint_x: 1
                    height: dp(48)
                    size_hint_y: None
                    opacity: 0
                    disabled: True
                    on_release: root.go_admin()

                MDRaisedButton:
                    text: 'Sign Out'
                    md_bg_color: 0.937, 0.278, 0.435, 0.8
                    size_hint_x: 1
                    height: dp(48)
                    size_hint_y: None
                    on_release: root.logout()
'''

Builder.load_string(KV)


class ProfileScreen(MDScreen):
    def on_enter(self):
        from kivymd.app import MDApp
        from services.question_service import get_rank
        app = MDApp.get_running_app()
        user = app.current_user
        if not user:
            self.manager.current = 'login'
            return
        self.ids.avatar_icon.text = user['username'][0].upper()
        self.ids.username_lbl.text = user['username']
        self.ids.email_lbl.text = user['email']
        self.ids.rank_lbl.text = get_rank(user.get('total_score', 0))
        self.ids.games_lbl.text = str(user.get('games_played', 0))
        self.ids.score_lbl.text = str(user.get('total_score', 0))

        # Language buttons
        lang = app.lang
        self.ids.btn_en.md_bg_color = (0.424, 0.388, 1, 1) if lang == 'en' else (0.082, 0.094, 0.204, 1)
        self.ids.btn_fr.md_bg_color = (0.424, 0.388, 1, 1) if lang == 'fr' else (0.082, 0.094, 0.204, 1)

        # Admin button
        if user.get('is_admin'):
            self.ids.admin_btn.opacity = 1
            self.ids.admin_btn.disabled = False
        else:
            self.ids.admin_btn.opacity = 0
            self.ids.admin_btn.disabled = True

    def set_lang(self, lang):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        app.lang = lang
        self.ids.btn_en.md_bg_color = (0.424, 0.388, 1, 1) if lang == 'en' else (0.082, 0.094, 0.204, 1)
        self.ids.btn_fr.md_bg_color = (0.424, 0.388, 1, 1) if lang == 'fr' else (0.082, 0.094, 0.204, 1)

    def go_admin(self):
        self.manager.current = 'admin_dashboard'

    def logout(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        app.current_user = None
        self.manager.current = 'menu'

    def go_back(self):
        self.manager.current = 'menu'
