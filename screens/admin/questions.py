from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDRaisedButton, MDFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar

KV = '''
<AdminQuestionsScreen>:
    name: 'admin_questions'
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
                text: 'Questions'
                font_style: 'H6'
                theme_text_color: 'Custom'
                text_color: 1, 1, 1, 1

            MDIconButton:
                icon: 'plus'
                theme_icon_color: 'Custom'
                icon_color: 0.024, 0.839, 0.627, 1
                on_release: root.add_question()

        # Search bar
        MDBoxLayout:
            size_hint_y: None
            height: dp(52)
            padding: dp(8), dp(4)
            canvas.before:
                Color:
                    rgba: 0.055, 0.071, 0.184, 0.6
                Rectangle:
                    pos: self.pos
                    size: self.size

            MDTextField:
                id: search_field
                hint_text: 'Search questions...'
                mode: 'rectangle'
                size_hint_y: None
                height: dp(44)
                on_text_validate: root.do_search()

            MDIconButton:
                icon: 'magnify'
                theme_icon_color: 'Custom'
                icon_color: 0.424, 0.388, 1, 1
                size_hint_x: None
                width: dp(44)
                on_release: root.do_search()

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

        # Pagination info
        MDBoxLayout:
            size_hint_y: None
            height: dp(32)
            padding: dp(12), dp(4)

            MDLabel:
                id: page_info
                text: ''
                font_style: 'Caption'
                theme_text_color: 'Custom'
                text_color: 0.533, 0.569, 0.69, 1

            MDBoxLayout:
                orientation: 'horizontal'
                size_hint_x: None
                width: dp(80)
                spacing: dp(4)

                MDIconButton:
                    icon: 'chevron-left'
                    size_hint: None, None
                    size: dp(28), dp(28)
                    theme_icon_color: 'Custom'
                    icon_color: 0.424, 0.388, 1, 1
                    on_release: root.prev_page()

                MDIconButton:
                    icon: 'chevron-right'
                    size_hint: None, None
                    size: dp(28), dp(28)
                    theme_icon_color: 'Custom'
                    icon_color: 0.424, 0.388, 1, 1
                    on_release: root.next_page()

        ScrollView:
            MDBoxLayout:
                id: q_list
                orientation: 'vertical'
                spacing: dp(6)
                padding: dp(10)
                adaptive_height: True


<AdminQuestionFormScreen>:
    name: 'admin_question_form'
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
                icon: 'close'
                theme_icon_color: 'Custom'
                icon_color: 1, 1, 1, 1
                on_release: root.go_back()

            MDLabel:
                id: form_title
                text: 'New Question'
                font_style: 'H6'
                theme_text_color: 'Custom'
                text_color: 1, 1, 1, 1

            MDIconButton:
                icon: 'content-save'
                theme_icon_color: 'Custom'
                icon_color: 0.024, 0.839, 0.627, 1
                on_release: root.save_question()

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(12)
                padding: dp(16)
                adaptive_height: True

                MDTextField:
                    id: f_category
                    hint_text: 'Category (capitals/currencies/presidents/geography/monuments/sports/music)'
                    mode: 'rectangle'
                    size_hint_y: None
                    height: dp(56)

                MDTextField:
                    id: f_question_en
                    hint_text: 'Question (English)'
                    mode: 'rectangle'
                    multiline: True
                    size_hint_y: None
                    height: dp(80)

                MDTextField:
                    id: f_question_fr
                    hint_text: 'Question (French)'
                    mode: 'rectangle'
                    multiline: True
                    size_hint_y: None
                    height: dp(80)

                MDTextField:
                    id: f_answer
                    hint_text: 'Correct Answer'
                    mode: 'rectangle'
                    size_hint_y: None
                    height: dp(56)

                MDTextField:
                    id: f_option1
                    hint_text: 'Wrong option 1'
                    mode: 'rectangle'
                    size_hint_y: None
                    height: dp(56)

                MDTextField:
                    id: f_option2
                    hint_text: 'Wrong option 2'
                    mode: 'rectangle'
                    size_hint_y: None
                    height: dp(56)

                MDTextField:
                    id: f_option3
                    hint_text: 'Wrong option 3'
                    mode: 'rectangle'
                    size_hint_y: None
                    height: dp(56)

                MDTextField:
                    id: f_continent
                    hint_text: 'Continent (Africa/Americas/Asia/Europe/Oceania)'
                    mode: 'rectangle'
                    size_hint_y: None
                    height: dp(56)

                MDTextField:
                    id: f_country
                    hint_text: 'Country'
                    mode: 'rectangle'
                    size_hint_y: None
                    height: dp(56)

                MDTextField:
                    id: f_difficulty
                    hint_text: 'Difficulty (easy/medium/hard)'
                    mode: 'rectangle'
                    size_hint_y: None
                    height: dp(56)

                MDTextField:
                    id: f_hint_en
                    hint_text: 'Hint (English, optional)'
                    mode: 'rectangle'
                    size_hint_y: None
                    height: dp(56)

                MDTextField:
                    id: f_hint_fr
                    hint_text: 'Hint (French, optional)'
                    mode: 'rectangle'
                    size_hint_y: None
                    height: dp(56)

                Widget:
                    size_hint_y: None
                    height: dp(20)
'''

Builder.load_string(KV)

CATEGORIES = ['All', 'capitals', 'currencies', 'presidents', 'geography', 'monuments', 'sports', 'music']
PER_PAGE = 20


class AdminQuestionsScreen(MDScreen):
    current_page = 1
    total_questions = 0
    selected_category = ''
    search_text = ''

    def on_enter(self):
        self._build_filter()
        self._load_questions()

    def _build_filter(self):
        row = self.ids.cat_filter
        row.clear_widgets()
        for c in CATEGORIES:
            btn = MDRaisedButton(
                text=c.capitalize(), size_hint=None,
                height=dp(32), font_size='11sp',
            )
            btn.width = dp(max(55, len(c) * 9 + 16))
            cat_val = '' if c == 'All' else c
            if cat_val == self.selected_category:
                btn.md_bg_color = (0.424, 0.388, 1, 1)
            else:
                btn.md_bg_color = (0.082, 0.094, 0.204, 1)
            btn.bind(on_release=lambda x, cat=cat_val: self.filter_category(cat))
            row.add_widget(btn)

    def _load_questions(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        rows, total = app.db.get_all_questions(
            category=self.selected_category,
            search=self.search_text,
            page=self.current_page,
            per_page=PER_PAGE,
        )
        self.total_questions = total
        total_pages = max(1, (total + PER_PAGE - 1) // PER_PAGE)
        self.ids.page_info.text = (f'Page {self.current_page}/{total_pages} '
                                   f'({total} questions)')
        lst = self.ids.q_list
        lst.clear_widgets()
        if not rows:
            lst.add_widget(MDLabel(
                text='No questions found.',
                halign='center',
                theme_text_color='Custom',
                text_color=(0.533, 0.569, 0.69, 1),
                size_hint_y=None, height=dp(60),
            ))
            return
        for q in rows:
            card = self._make_question_card(q)
            lst.add_widget(card)

    def _make_question_card(self, q):
        card = MDCard(
            orientation='vertical', padding=dp(10), spacing=dp(4),
            size_hint_y=None, height=dp(88),
            md_bg_color=(0.082, 0.094, 0.204, 1), radius=[dp(10)],
        )
        top_row = BoxLayout(orientation='horizontal', spacing=dp(4), size_hint_y=None, height=dp(36))
        q_lbl = MDLabel(
            text=q['question_en'][:60] + ('...' if len(q['question_en']) > 60 else ''),
            theme_text_color='Custom', text_color=(1, 1, 1, 1),
            font_style='Subtitle2',
        )
        top_row.add_widget(q_lbl)

        edit_btn = MDIconButton(
            icon='pencil', size_hint=None, size=(dp(36), dp(36)),
            theme_icon_color='Custom', icon_color=(1, 0.718, 0.012, 1),
        )
        qid = q['id']
        edit_btn.bind(on_release=lambda x, i=qid: self.edit_question(i))

        del_btn = MDIconButton(
            icon='delete', size_hint=None, size=(dp(36), dp(36)),
            theme_icon_color='Custom', icon_color=(0.937, 0.278, 0.435, 1),
        )
        del_btn.bind(on_release=lambda x, i=qid: self.confirm_delete(i))

        toggle_btn = MDIconButton(
            icon='eye' if q.get('is_active', 1) else 'eye-off',
            size_hint=None, size=(dp(36), dp(36)),
            theme_icon_color='Custom',
            icon_color=(0.024, 0.839, 0.627, 1) if q.get('is_active', 1) else (0.533, 0.569, 0.69, 1),
        )
        toggle_btn.bind(on_release=lambda x, i=qid: self.toggle_question(i))

        top_row.add_widget(toggle_btn)
        top_row.add_widget(edit_btn)
        top_row.add_widget(del_btn)

        bottom_row = BoxLayout(orientation='horizontal', spacing=dp(8), size_hint_y=None, height=dp(24))
        for text, color in [
            (q.get('category', ''), (0.424, 0.388, 1, 1)),
            (q.get('continent', ''), (0.024, 0.839, 0.627, 0.8)),
            (f"A: {q.get('answer', '')[:20]}", (1, 0.718, 0.012, 1)),
        ]:
            bottom_row.add_widget(MDLabel(
                text=text, theme_text_color='Custom', text_color=color, font_style='Caption',
            ))

        card.add_widget(top_row)
        card.add_widget(bottom_row)
        return card

    def filter_category(self, category):
        self.selected_category = category
        self.current_page = 1
        self._build_filter()
        self._load_questions()

    def do_search(self):
        self.search_text = self.ids.search_field.text.strip()
        self.current_page = 1
        self._load_questions()

    def next_page(self):
        total_pages = max(1, (self.total_questions + PER_PAGE - 1) // PER_PAGE)
        if self.current_page < total_pages:
            self.current_page += 1
            self._load_questions()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self._load_questions()

    def add_question(self):
        from kivymd.app import MDApp
        MDApp.get_running_app().editing_question_id = None
        self.manager.current = 'admin_question_form'

    def edit_question(self, qid):
        from kivymd.app import MDApp
        MDApp.get_running_app().editing_question_id = qid
        self.manager.current = 'admin_question_form'

    def confirm_delete(self, qid):
        self._pending_delete_id = qid
        self._dialog = MDDialog(
            title='Delete Question',
            text='Are you sure you want to delete this question?',
            buttons=[
                MDFlatButton(text='Cancel', on_release=lambda x: self._dialog.dismiss()),
                MDRaisedButton(
                    text='Delete', md_bg_color=(0.937, 0.278, 0.435, 1),
                    on_release=lambda x: self._do_delete(),
                ),
            ],
        )
        self._dialog.open()

    def _do_delete(self):
        from kivymd.app import MDApp
        self._dialog.dismiss()
        MDApp.get_running_app().db.delete_question(self._pending_delete_id)
        Snackbar(text='Question deleted.', snackbar_x='10dp', snackbar_y='10dp',
                 size_hint_x=0.9, bg_color=(0.024, 0.839, 0.627, 1)).open()
        self._load_questions()

    def toggle_question(self, qid):
        from kivymd.app import MDApp
        MDApp.get_running_app().db.toggle_question(qid)
        self._load_questions()

    def go_back(self):
        self.manager.current = 'admin_dashboard'


class AdminQuestionFormScreen(MDScreen):
    def on_enter(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        qid = app.editing_question_id
        fields = ['f_category', 'f_question_en', 'f_question_fr', 'f_answer',
                  'f_option1', 'f_option2', 'f_option3', 'f_continent',
                  'f_country', 'f_difficulty', 'f_hint_en', 'f_hint_fr']
        if qid:
            self.ids.form_title.text = 'Edit Question'
            q = app.db.get_question(qid)
            if q:
                mapping = {
                    'f_category': 'category', 'f_question_en': 'question_en',
                    'f_question_fr': 'question_fr', 'f_answer': 'answer',
                    'f_option1': 'option1', 'f_option2': 'option2',
                    'f_option3': 'option3', 'f_continent': 'continent',
                    'f_country': 'country', 'f_difficulty': 'difficulty',
                    'f_hint_en': 'hint_en', 'f_hint_fr': 'hint_fr',
                }
                for fid, key in mapping.items():
                    self.ids[fid].text = str(q.get(key, '') or '')
        else:
            self.ids.form_title.text = 'New Question'
            for fid in fields:
                self.ids[fid].text = ''
            self.ids.f_difficulty.text = 'medium'

    def save_question(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        data = {
            'category':    self.ids.f_category.text.strip(),
            'question_en': self.ids.f_question_en.text.strip(),
            'question_fr': self.ids.f_question_fr.text.strip(),
            'answer':      self.ids.f_answer.text.strip(),
            'option1':     self.ids.f_option1.text.strip(),
            'option2':     self.ids.f_option2.text.strip(),
            'option3':     self.ids.f_option3.text.strip(),
            'continent':   self.ids.f_continent.text.strip(),
            'country':     self.ids.f_country.text.strip(),
            'difficulty':  self.ids.f_difficulty.text.strip() or 'medium',
            'hint_en':     self.ids.f_hint_en.text.strip(),
            'hint_fr':     self.ids.f_hint_fr.text.strip(),
        }
        if not data['category'] or not data['question_en'] or not data['answer']:
            Snackbar(text='Category, question, and answer are required.',
                     snackbar_x='10dp', snackbar_y='10dp', size_hint_x=0.9,
                     bg_color=(0.937, 0.278, 0.435, 1)).open()
            return
        if not all([data['option1'], data['option2'], data['option3']]):
            Snackbar(text='Please provide 3 wrong options.',
                     snackbar_x='10dp', snackbar_y='10dp', size_hint_x=0.9,
                     bg_color=(0.937, 0.278, 0.435, 1)).open()
            return

        qid = app.editing_question_id
        if qid:
            app.db.update_question(qid, data)
            msg = 'Question updated!'
        else:
            app.db.create_question(data)
            msg = 'Question created!'

        Snackbar(text=msg, snackbar_x='10dp', snackbar_y='10dp',
                 size_hint_x=0.9, bg_color=(0.024, 0.839, 0.627, 1)).open()
        self.manager.current = 'admin_questions'

    def go_back(self):
        self.manager.current = 'admin_questions'
