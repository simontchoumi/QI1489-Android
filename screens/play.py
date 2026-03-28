import random
import time
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.animation import Animation
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout

KV = '''
<PlayScreen>:
    name: 'play'
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
            height: dp(52)
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
                icon_color: 1, 0.396, 0.518, 1
                on_release: root.quit_game()

            MDLabel:
                id: cat_label
                text: 'QI1489'
                halign: 'center'
                font_style: 'H6'
                theme_text_color: 'Custom'
                text_color: 1, 1, 1, 1

            MDLabel:
                id: score_label
                text: '0'
                halign: 'right'
                size_hint_x: None
                width: dp(60)
                font_style: 'Subtitle1'
                theme_text_color: 'Custom'
                text_color: 1, 0.718, 0.012, 1

        # Progress row
        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(32)
            padding: dp(12), dp(4)
            spacing: dp(8)

            MDLabel:
                id: progress_label
                text: 'Q 1 / 10'
                size_hint_x: None
                width: dp(70)
                font_style: 'Caption'
                theme_text_color: 'Custom'
                text_color: 0.533, 0.569, 0.69, 1

            MDProgressBar:
                id: progress_bar
                value: 0
                max: 100
                color: 0.424, 0.388, 1, 1

        # Timer bar
        MDBoxLayout:
            size_hint_y: None
            height: dp(6)
            padding: 0

            MDProgressBar:
                id: timer_bar
                value: 100
                max: 100
                color: 0.024, 0.839, 0.627, 1

        # Question card
        ScrollView:
            size_hint_y: None
            height: dp(130)
            do_scroll_x: False

            MDCard:
                id: question_card
                orientation: 'vertical'
                padding: dp(16)
                spacing: dp(8)
                size_hint_y: None
                height: dp(130)
                md_bg_color: 0.082, 0.094, 0.204, 1
                radius: [0]

                MDLabel:
                    id: question_text
                    text: ''
                    halign: 'center'
                    theme_text_color: 'Custom'
                    text_color: 1, 1, 1, 1
                    font_style: 'H6'

        # Options
        ScrollView:
            MDBoxLayout:
                id: options_box
                orientation: 'vertical'
                spacing: dp(10)
                padding: dp(12)
                adaptive_height: True

        Widget:
'''

Builder.load_string(KV)

OPTION_COLORS = [
    (0.424, 0.388, 1, 1),    # purple
    (0.024, 0.839, 0.627, 1), # green
    (1, 0.718, 0.012, 1),    # amber
    (0.067, 0.541, 0.698, 1), # blue
]


class OptionButton(MDRaisedButton):
    def __init__(self, text, color, index, on_select, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.md_bg_color = color
        self.index = index
        self.on_select = on_select
        self.size_hint_y = None
        self.height = dp(52)
        self.font_size = '15sp'
        self.bind(on_release=self._selected)

    def _selected(self, *args):
        self.on_select(self.text)


class PlayScreen(MDScreen):
    def on_enter(self):
        from kivymd.app import MDApp
        self.app = MDApp.get_running_app()
        self.lang = self.app.lang
        self.game_data = self.app.game_data or {}
        self.questions = []
        self.current_index = 0
        self.correct_count = 0
        self.start_time = time.time()
        self.timer_event = None
        self.answered = False
        self.time_per_q = int(self.app.db.get_setting('question_time', '15'))
        self.questions_per_game = int(self.app.db.get_setting('questions_per_game', '10'))
        self.time_left = self.time_per_q
        self._load_questions()

    def _load_questions(self):
        from services.question_service import get_questions, get_geography_questions
        cat = self.game_data.get('category', 'capitals')
        continent = self.game_data.get('continent', 'Worldwide')
        if cat == 'geography':
            self.questions = get_geography_questions(self.app.db, self.questions_per_game, self.lang)
        else:
            self.questions = get_questions(self.app.db, cat, continent, self.questions_per_game, self.lang)
        if not self.questions:
            self._show_no_questions()
            return
        self.ids.cat_label.text = cat.capitalize()
        self._show_question()

    def _show_no_questions(self):
        self.ids.question_text.text = 'No questions available.\nTry updating the database.'
        self.ids.options_box.clear_widgets()

    def _show_question(self):
        if self.current_index >= len(self.questions):
            self._finish_game()
            return
        q = self.questions[self.current_index]
        self.answered = False
        self.time_left = self.time_per_q

        # Labels
        total = len(self.questions)
        self.ids.progress_label.text = f'Q {self.current_index + 1} / {total}'
        self.ids.progress_bar.value = (self.current_index / total) * 100
        self.ids.question_text.text = q['question']
        self.ids.score_label.text = str(self._calc_current_score())
        self.ids.timer_bar.color = (0.024, 0.839, 0.627, 1)

        # Options
        box = self.ids.options_box
        box.clear_widgets()
        for i, opt in enumerate(q['options']):
            btn = OptionButton(
                text=opt,
                color=OPTION_COLORS[i % len(OPTION_COLORS)],
                index=i,
                on_select=self._answer_selected,
            )
            box.add_widget(btn)

        # Timer
        if self.timer_event:
            self.timer_event.cancel()
        self.timer_event = Clock.schedule_interval(self._tick_timer, 1)

    def _tick_timer(self, dt):
        self.time_left -= 1
        pct = (self.time_left / self.time_per_q) * 100
        self.ids.timer_bar.value = max(0, pct)
        # Color shift red when low
        if self.time_left <= 5:
            self.ids.timer_bar.color = (0.937, 0.278, 0.435, 1)
        if self.time_left <= 0:
            if self.timer_event:
                self.timer_event.cancel()
            if not self.answered:
                self._answer_selected(None)  # timeout

    def _answer_selected(self, selected_text):
        if self.answered:
            return
        self.answered = True
        if self.timer_event:
            self.timer_event.cancel()

        q = self.questions[self.current_index]
        correct = q['answer']
        is_correct = (selected_text == correct)

        if is_correct:
            self.correct_count += 1

        # Visual feedback on buttons
        box = self.ids.options_box
        for btn in box.children:
            if isinstance(btn, OptionButton):
                if btn.text == correct:
                    btn.md_bg_color = (0.024, 0.839, 0.627, 1)  # green = correct
                elif btn.text == selected_text:
                    btn.md_bg_color = (0.937, 0.278, 0.435, 1)  # red = wrong
                else:
                    btn.md_bg_color = (0.2, 0.2, 0.3, 1)  # grey out

        # Increment shown count
        self.app.db.increment_question_shown(q['id'])

        # Next question after delay
        Clock.schedule_once(self._next_question, 1.5)

    def _next_question(self, dt):
        self.current_index += 1
        self._show_question()

    def _calc_current_score(self):
        from services.question_service import calculate_score
        elapsed = int(time.time() - self.start_time)
        return calculate_score(self.correct_count, max(self.current_index, 1), elapsed)

    def _finish_game(self):
        from services.question_service import calculate_score
        import uuid
        elapsed = int(time.time() - self.start_time)
        total = len(self.questions)
        score = calculate_score(self.correct_count, total, elapsed)
        max_possible = total * 15

        user_id = self.app.current_user['id'] if self.app.current_user else None
        guest_token = self.app.guest_token
        if not guest_token and not user_id:
            self.app.guest_token = str(uuid.uuid4())
            guest_token = self.app.guest_token

        score_id = self.app.db.save_score(
            user_id=user_id,
            guest_token=guest_token if not user_id else None,
            guest_name='Guest',
            category=self.game_data.get('category', ''),
            continent=self.game_data.get('continent', 'Worldwide'),
            score=score,
            max_possible=max_possible,
            questions_answered=total,
            correct_answers=self.correct_count,
            time_played=elapsed,
        )
        if user_id:
            self.app.db.update_user_stats(user_id, score)

        self.app.last_score_id = score_id
        self.app.last_score = {
            'score': score, 'correct': self.correct_count,
            'total': total, 'time_played': elapsed,
            'category': self.game_data.get('category', ''),
        }
        self.manager.current = 'results'

    def quit_game(self):
        if self.timer_event:
            self.timer_event.cancel()
        self.manager.current = 'menu'
