from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivy.uix.boxlayout import BoxLayout

KV = '''
<MenuScreen>:
    name: 'menu'
    canvas.before:
        Color:
            rgba: 0.039, 0.055, 0.153, 1
        Rectangle:
            pos: self.pos
            size: self.size

    MDBoxLayout:
        orientation: 'vertical'
        spacing: 0

        # Top bar
        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(56)
            padding: dp(8), dp(4)
            spacing: dp(4)
            canvas.before:
                Color:
                    rgba: 0.055, 0.071, 0.184, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            MDLabel:
                text: 'QI[color=#FFB703]1489[/color]'
                markup: True
                font_style: 'H6'
                theme_text_color: 'Custom'
                text_color: 1, 1, 1, 1
                size_hint_x: 1

            MDIconButton:
                id: lang_btn
                icon: 'translate'
                theme_icon_color: 'Custom'
                icon_color: 0.424, 0.388, 1, 1
                on_release: root.toggle_lang()

            MDIconButton:
                id: profile_btn
                icon: 'account-circle'
                theme_icon_color: 'Custom'
                icon_color: 0.424, 0.388, 1, 1
                on_release: root.go_profile()

        # Continent selector
        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(48)
            padding: dp(8), dp(4)
            spacing: dp(6)
            canvas.before:
                Color:
                    rgba: 0.055, 0.071, 0.184, 0.8
                Rectangle:
                    pos: self.pos
                    size: self.size

            MDLabel:
                text: 'Region:'
                size_hint_x: None
                width: dp(60)
                theme_text_color: 'Custom'
                text_color: 0.533, 0.569, 0.69, 1
                font_style: 'Caption'

            ScrollView:
                do_scroll_y: False
                do_scroll_x: True
                bar_width: 0

                MDBoxLayout:
                    id: continent_row
                    orientation: 'horizontal'
                    spacing: dp(6)
                    padding: dp(2)
                    size_hint_x: None
                    width: self.minimum_width
                    adaptive_height: True

        # Scroll area for categories
        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(12)
                padding: dp(12)
                adaptive_height: True

                MDLabel:
                    id: title_label
                    text: 'Choose a Category'
                    halign: 'center'
                    font_style: 'H6'
                    theme_text_color: 'Custom'
                    text_color: 1, 1, 1, 1
                    size_hint_y: None
                    height: dp(36)

                GridLayout:
                    id: cat_grid
                    cols: 2
                    spacing: dp(10)
                    size_hint_y: None
                    height: self.minimum_height
                    adaptive_height: True

                MDBoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(10)
                    size_hint_y: None
                    height: dp(44)
                    padding: dp(4), 0

                    MDRaisedButton:
                        text: 'Leaderboard'
                        md_bg_color: 0.424, 0.388, 1, 1
                        size_hint_x: 1
                        on_release: root.go_leaderboard()

                MDLabel:
                    id: info_label
                    text: ''
                    halign: 'center'
                    font_style: 'Caption'
                    theme_text_color: 'Custom'
                    text_color: 0.533, 0.569, 0.69, 1
                    size_hint_y: None
                    height: dp(24)
'''

Builder.load_string(KV)

CATEGORIES = {
    'capitals':   {'en': 'Country Capitals',      'fr': 'Capitales',          'icon': 'city',           'color': (0.424, 0.388, 1, 1)},
    'currencies': {'en': 'Currencies',             'fr': 'Monnaies',           'icon': 'cash',           'color': (1, 0.718, 0.012, 1)},
    'presidents': {'en': 'World Leaders',          'fr': 'Dirigeants',         'icon': 'account-tie',    'color': (1, 0.396, 0.518, 1)},
    'geography':  {'en': 'Rivers & Seas',          'fr': 'Fleuves & Mers',     'icon': 'map',            'color': (0.024, 0.839, 0.627, 1)},
    'monuments':  {'en': 'Monuments',              'fr': 'Monuments',          'icon': 'bank',           'color': (0.937, 0.278, 0.435, 1)},
    'sports':     {'en': 'Sports Stars',           'fr': 'Stars du sport',     'icon': 'trophy',         'color': (0.067, 0.541, 0.698, 1)},
    'music':      {'en': 'Music Artists',          'fr': 'Artistes',           'icon': 'music',          'color': (0.969, 0.498, 0, 1)},
}

CONTINENTS = ['Worldwide', 'Africa', 'Americas', 'Asia', 'Europe', 'Oceania']


class CategoryCard(MDCard):
    def __init__(self, category, cat_info, lang, on_tap, **kwargs):
        super().__init__(**kwargs)
        self.category = category
        self.on_tap = on_tap
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(110)
        self.padding = dp(12)
        self.spacing = dp(6)
        self.md_bg_color = (0.082, 0.094, 0.204, 1)
        self.radius = [dp(14)]
        self.ripple_behavior = True

        icon_box = BoxLayout(size_hint_y=None, height=dp(44))
        icon_lbl = MDLabel(
            text=cat_info['en'][0],
            halign='center',
            font_style='H4',
            theme_text_color='Custom',
            text_color=cat_info['color'],
        )
        icon_box.add_widget(icon_lbl)
        self.add_widget(icon_box)

        name_lbl = MDLabel(
            text=cat_info[lang],
            halign='center',
            font_style='Subtitle2',
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(28),
        )
        self.add_widget(name_lbl)
        self.name_lbl = name_lbl
        self.bind(on_release=self._tapped)

    def _tapped(self, *args):
        self.on_tap(self.category)


class MenuScreen(MDScreen):
    selected_continent = 'Worldwide'

    def on_enter(self):
        self._build_ui()
        self._update_info()

    def _build_ui(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        lang = app.lang

        # Continent buttons
        row = self.ids.continent_row
        row.clear_widgets()
        for c in CONTINENTS:
            btn = MDRaisedButton(
                text=c,
                size_hint=None,
                height=dp(32),
                font_size='12sp',
            )
            btn.width = dp(max(80, len(c) * 8 + 20))
            if c == self.selected_continent:
                btn.md_bg_color = (0.424, 0.388, 1, 1)
            else:
                btn.md_bg_color = (0.082, 0.094, 0.204, 1)
            btn.bind(on_release=lambda x, continent=c: self.select_continent(continent))
            row.add_widget(btn)

        # Category grid
        grid = self.ids.cat_grid
        grid.clear_widgets()
        for cat_key, cat_info in CATEGORIES.items():
            card = CategoryCard(
                category=cat_key,
                cat_info=cat_info,
                lang=lang,
                on_tap=self.start_game,
            )
            grid.add_widget(card)

        # Labels
        self.ids.title_label.text = ('Choisissez une categorie' if lang == 'fr'
                                     else 'Choose a Category')
        # Profile button icon
        if app.current_user:
            self.ids.profile_btn.icon = 'account'
        else:
            self.ids.profile_btn.icon = 'account-circle-outline'

    def _update_info(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        stats = app.db.get_stats()
        total = stats.get('total_questions', 0)
        self.ids.info_label.text = f'{total} questions available'

    def select_continent(self, continent):
        self.selected_continent = continent
        self._build_ui()

    def start_game(self, category):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        app.game_data = {
            'category': category,
            'continent': self.selected_continent,
        }
        self.manager.current = 'play'

    def go_leaderboard(self):
        self.manager.current = 'leaderboard'

    def go_profile(self):
        self.manager.current = 'login'

    def toggle_lang(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        app.lang = 'fr' if app.lang == 'en' else 'en'
        self._build_ui()
