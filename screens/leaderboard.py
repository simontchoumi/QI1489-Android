from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivy.uix.boxlayout import BoxLayout

KV = '''
<LeaderboardScreen>:
    name: 'leaderboard'
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
                text: 'Leaderboard'
                font_style: 'H6'
                theme_text_color: 'Custom'
                text_color: 1, 1, 1, 1

        # Category filter
        ScrollView:
            size_hint_y: None
            height: dp(44)
            do_scroll_y: False

            MDBoxLayout:
                id: cat_filter
                orientation: 'horizontal'
                spacing: dp(6)
                padding: dp(8), dp(4)
                size_hint_x: None
                width: self.minimum_width
                adaptive_height: True

        ScrollView:
            MDBoxLayout:
                id: lb_list
                orientation: 'vertical'
                spacing: dp(6)
                padding: dp(12)
                adaptive_height: True
'''

Builder.load_string(KV)

RANK_ICONS = ['1', '2', '3']
RANK_COLORS = [
    (1, 0.718, 0.012, 1),   # gold
    (0.753, 0.753, 0.753, 1), # silver
    (0.804, 0.498, 0.196, 1), # bronze
]


class LeaderboardScreen(MDScreen):
    selected_category = None

    def on_enter(self):
        self._build_filter()
        self._load_data()

    def _build_filter(self):
        from kivymd.app import MDApp
        from kivymd.uix.button import MDRaisedButton
        row = self.ids.cat_filter
        row.clear_widgets()
        categories = ['All', 'capitals', 'currencies', 'presidents',
                      'geography', 'monuments', 'sports', 'music']
        for c in categories:
            btn = MDRaisedButton(
                text=c.capitalize(),
                size_hint=None,
                height=dp(32),
                font_size='11sp',
            )
            btn.width = dp(max(60, len(c) * 9 + 16))
            if (c == 'All' and not self.selected_category) or c == self.selected_category:
                btn.md_bg_color = (0.424, 0.388, 1, 1)
            else:
                btn.md_bg_color = (0.082, 0.094, 0.204, 1)
            cat_val = None if c == 'All' else c
            btn.bind(on_release=lambda x, cat=cat_val: self.filter_category(cat))
            row.add_widget(btn)

    def _load_data(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        entries = app.db.get_leaderboard(category=self.selected_category, limit=50)
        lst = self.ids.lb_list
        lst.clear_widgets()
        if not entries:
            lbl = MDLabel(
                text='No scores yet. Play a game!',
                halign='center',
                theme_text_color='Custom',
                text_color=(0.533, 0.569, 0.69, 1),
                size_hint_y=None, height=dp(60),
            )
            lst.add_widget(lbl)
            return
        for i, entry in enumerate(entries):
            card = self._make_entry(i, entry)
            lst.add_widget(card)

    def _make_entry(self, i, entry):
        card = MDCard(
            orientation='horizontal',
            padding=dp(12),
            spacing=dp(10),
            size_hint_y=None,
            height=dp(62),
            md_bg_color=(0.082, 0.094, 0.204, 1),
            radius=[dp(10)],
        )
        rank_color = RANK_COLORS[i] if i < 3 else (0.533, 0.569, 0.69, 1)
        rank_lbl = MDLabel(
            text=f'#{i+1}',
            theme_text_color='Custom',
            text_color=rank_color,
            font_style='H6',
            size_hint_x=None, width=dp(42),
            halign='center',
        )
        card.add_widget(rank_lbl)

        info_box = BoxLayout(orientation='vertical', spacing=dp(2))
        name_lbl = MDLabel(
            text=entry.get('display_name', 'Guest'),
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1),
            font_style='Subtitle2',
        )
        cat_lbl = MDLabel(
            text=f"{entry.get('category', '')} · {entry.get('continent', 'Worldwide')}",
            theme_text_color='Custom',
            text_color=(0.533, 0.569, 0.69, 1),
            font_style='Caption',
        )
        info_box.add_widget(name_lbl)
        info_box.add_widget(cat_lbl)
        card.add_widget(info_box)

        score_lbl = MDLabel(
            text=str(entry.get('score', 0)),
            theme_text_color='Custom',
            text_color=(1, 0.718, 0.012, 1),
            font_style='H6',
            size_hint_x=None, width=dp(60),
            halign='right',
        )
        card.add_widget(score_lbl)
        return card

    def filter_category(self, category):
        self.selected_category = category
        self._build_filter()
        self._load_data()

    def go_back(self):
        self.manager.current = 'menu'
