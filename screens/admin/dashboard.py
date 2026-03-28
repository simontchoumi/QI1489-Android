from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDIconButton

KV = '''
<AdminDashboardScreen>:
    name: 'admin_dashboard'
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
                text: 'Admin Dashboard'
                font_style: 'H6'
                theme_text_color: 'Custom'
                text_color: 1, 0.718, 0.012, 1

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(16)
                padding: dp(16)
                adaptive_height: True

                Widget:
                    size_hint_y: None
                    height: dp(8)

                # Stats row
                MDBoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(10)
                    size_hint_y: None
                    height: dp(88)

                    MDCard:
                        orientation: 'vertical'
                        padding: dp(12)
                        spacing: dp(4)
                        md_bg_color: 0.082, 0.094, 0.204, 1
                        radius: [dp(12)]

                        MDLabel:
                            id: stat_questions
                            text: '0'
                            halign: 'center'
                            font_style: 'H5'
                            theme_text_color: 'Custom'
                            text_color: 0.424, 0.388, 1, 1

                        MDLabel:
                            text: 'Questions'
                            halign: 'center'
                            font_style: 'Caption'
                            theme_text_color: 'Custom'
                            text_color: 0.533, 0.569, 0.69, 1

                    MDCard:
                        orientation: 'vertical'
                        padding: dp(12)
                        spacing: dp(4)
                        md_bg_color: 0.082, 0.094, 0.204, 1
                        radius: [dp(12)]

                        MDLabel:
                            id: stat_users
                            text: '0'
                            halign: 'center'
                            font_style: 'H5'
                            theme_text_color: 'Custom'
                            text_color: 1, 0.718, 0.012, 1

                        MDLabel:
                            text: 'Users'
                            halign: 'center'
                            font_style: 'Caption'
                            theme_text_color: 'Custom'
                            text_color: 0.533, 0.569, 0.69, 1

                    MDCard:
                        orientation: 'vertical'
                        padding: dp(12)
                        spacing: dp(4)
                        md_bg_color: 0.082, 0.094, 0.204, 1
                        radius: [dp(12)]

                        MDLabel:
                            id: stat_games
                            text: '0'
                            halign: 'center'
                            font_style: 'H5'
                            theme_text_color: 'Custom'
                            text_color: 0.024, 0.839, 0.627, 1

                        MDLabel:
                            text: 'Games'
                            halign: 'center'
                            font_style: 'Caption'
                            theme_text_color: 'Custom'
                            text_color: 0.533, 0.569, 0.69, 1

                # Nav cards
                MDLabel:
                    text: 'Manage'
                    font_style: 'Subtitle1'
                    theme_text_color: 'Custom'
                    text_color: 0.533, 0.569, 0.69, 1
                    size_hint_y: None
                    height: dp(30)

                MDCard:
                    orientation: 'horizontal'
                    padding: dp(16)
                    spacing: dp(12)
                    size_hint_y: None
                    height: dp(68)
                    md_bg_color: 0.082, 0.094, 0.204, 1
                    radius: [dp(12)]
                    ripple_behavior: True
                    on_release: root.go_questions()

                    MDIcon:
                        icon: 'help-circle-outline'
                        theme_icon_color: 'Custom'
                        icon_color: 0.424, 0.388, 1, 1
                        size_hint_x: None
                        width: dp(36)

                    MDBoxLayout:
                        orientation: 'vertical'
                        spacing: dp(2)

                        MDLabel:
                            text: 'Questions'
                            font_style: 'Subtitle1'
                            theme_text_color: 'Custom'
                            text_color: 1, 1, 1, 1

                        MDLabel:
                            text: 'Add, edit, delete questions'
                            font_style: 'Caption'
                            theme_text_color: 'Custom'
                            text_color: 0.533, 0.569, 0.69, 1

                    MDIcon:
                        icon: 'chevron-right'
                        theme_icon_color: 'Custom'
                        icon_color: 0.533, 0.569, 0.69, 1
                        size_hint_x: None
                        width: dp(24)

                MDCard:
                    orientation: 'horizontal'
                    padding: dp(16)
                    spacing: dp(12)
                    size_hint_y: None
                    height: dp(68)
                    md_bg_color: 0.082, 0.094, 0.204, 1
                    radius: [dp(12)]
                    ripple_behavior: True
                    on_release: root.go_users()

                    MDIcon:
                        icon: 'account-group'
                        theme_icon_color: 'Custom'
                        icon_color: 1, 0.718, 0.012, 1
                        size_hint_x: None
                        width: dp(36)

                    MDBoxLayout:
                        orientation: 'vertical'
                        spacing: dp(2)

                        MDLabel:
                            text: 'Users'
                            font_style: 'Subtitle1'
                            theme_text_color: 'Custom'
                            text_color: 1, 1, 1, 1

                        MDLabel:
                            text: 'Manage user accounts'
                            font_style: 'Caption'
                            theme_text_color: 'Custom'
                            text_color: 0.533, 0.569, 0.69, 1

                    MDIcon:
                        icon: 'chevron-right'
                        theme_icon_color: 'Custom'
                        icon_color: 0.533, 0.569, 0.69, 1
                        size_hint_x: None
                        width: dp(24)

                MDCard:
                    orientation: 'horizontal'
                    padding: dp(16)
                    spacing: dp(12)
                    size_hint_y: None
                    height: dp(68)
                    md_bg_color: 0.082, 0.094, 0.204, 1
                    radius: [dp(12)]
                    ripple_behavior: True
                    on_release: root.go_settings()

                    MDIcon:
                        icon: 'cog'
                        theme_icon_color: 'Custom'
                        icon_color: 0.024, 0.839, 0.627, 1
                        size_hint_x: None
                        width: dp(36)

                    MDBoxLayout:
                        orientation: 'vertical'
                        spacing: dp(2)

                        MDLabel:
                            text: 'Settings'
                            font_style: 'Subtitle1'
                            theme_text_color: 'Custom'
                            text_color: 1, 1, 1, 1

                        MDLabel:
                            text: 'Game config, disclaimer, update DB'
                            font_style: 'Caption'
                            theme_text_color: 'Custom'
                            text_color: 0.533, 0.569, 0.69, 1

                    MDIcon:
                        icon: 'chevron-right'
                        theme_icon_color: 'Custom'
                        icon_color: 0.533, 0.569, 0.69, 1
                        size_hint_x: None
                        width: dp(24)

                # Recent scores
                MDLabel:
                    text: 'Recent Scores'
                    font_style: 'Subtitle1'
                    theme_text_color: 'Custom'
                    text_color: 0.533, 0.569, 0.69, 1
                    size_hint_y: None
                    height: dp(30)

                MDBoxLayout:
                    id: recent_scores
                    orientation: 'vertical'
                    spacing: dp(6)
                    adaptive_height: True
'''

Builder.load_string(KV)


class AdminDashboardScreen(MDScreen):
    def on_enter(self):
        from kivymd.app import MDApp
        from kivymd.uix.card import MDCard
        from kivymd.uix.label import MDLabel
        from kivy.uix.boxlayout import BoxLayout

        app = MDApp.get_running_app()
        if not app.current_user or not app.current_user.get('is_admin'):
            self.manager.current = 'menu'
            return

        stats = app.db.get_stats()
        self.ids.stat_questions.text = str(stats.get('total_questions', 0))
        self.ids.stat_users.text = str(stats.get('total_users', 0))
        self.ids.stat_games.text = str(stats.get('total_games', 0))

        scores_box = self.ids.recent_scores
        scores_box.clear_widgets()
        for s in app.db.get_recent_scores(8):
            card = MDCard(
                orientation='horizontal', padding=dp(10), spacing=dp(8),
                size_hint_y=None, height=dp(52),
                md_bg_color=(0.082, 0.094, 0.204, 1), radius=[dp(8)],
            )
            info = BoxLayout(orientation='vertical', spacing=dp(2))
            info.add_widget(MDLabel(
                text=s.get('display_name', 'Guest'),
                theme_text_color='Custom', text_color=(1, 1, 1, 1),
                font_style='Subtitle2',
            ))
            info.add_widget(MDLabel(
                text=f"{s.get('category', '')} · {s.get('created_at', '')[:10]}",
                theme_text_color='Custom', text_color=(0.533, 0.569, 0.69, 1),
                font_style='Caption',
            ))
            card.add_widget(info)
            card.add_widget(MDLabel(
                text=str(s.get('score', 0)),
                theme_text_color='Custom', text_color=(1, 0.718, 0.012, 1),
                font_style='H6', size_hint_x=None, width=dp(56), halign='right',
            ))
            scores_box.add_widget(card)

    def go_questions(self):
        self.manager.current = 'admin_questions'

    def go_users(self):
        self.manager.current = 'admin_users'

    def go_settings(self):
        self.manager.current = 'admin_settings'

    def go_back(self):
        self.manager.current = 'profile'
