"""
QI1489 — World Knowledge Quiz (Android / Desktop)
Copyright (c) Simon TCHOUMI NJANJOU | SMJx Game

Entry point. Launch with:
  python main.py          (desktop, for development)
  buildozer android debug (build APK)
"""
import os
import sys

# Fix encoding on Windows during development
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# KivyMD / Kivy env
os.environ.setdefault('KIVY_ORIENTATION', 'Portrait')

from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivymd.app import MDApp

# Import all screens
from screens.splash import SplashScreen
from screens.menu import MenuScreen
from screens.play import PlayScreen
from screens.results import ResultsScreen
from screens.leaderboard import LeaderboardScreen
from screens.auth import LoginScreen, RegisterScreen
from screens.profile import ProfileScreen
from screens.admin.dashboard import AdminDashboardScreen
from screens.admin.questions import AdminQuestionsScreen, AdminQuestionFormScreen
from screens.admin.users import AdminUsersScreen
from screens.admin.settings import AdminSettingsScreen

from database.db_manager import DatabaseManager


class QI1489App(MDApp):
    title = 'QI1489'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = DatabaseManager()
        self.current_user = None
        self.guest_token = None
        self.lang = 'en'
        self.game_data = {}
        self.last_score = {}
        self.last_score_id = None
        self.editing_question_id = None

    def build(self):
        # Theme
        self.theme_cls.primary_palette = 'DeepPurple'
        self.theme_cls.accent_palette = 'Amber'
        self.theme_cls.theme_style = 'Dark'

        sm = ScreenManager(transition=FadeTransition(duration=0.15))
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(PlayScreen(name='play'))
        sm.add_widget(ResultsScreen(name='results'))
        sm.add_widget(LeaderboardScreen(name='leaderboard'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(AdminDashboardScreen(name='admin_dashboard'))
        sm.add_widget(AdminQuestionsScreen(name='admin_questions'))
        sm.add_widget(AdminQuestionFormScreen(name='admin_question_form'))
        sm.add_widget(AdminUsersScreen(name='admin_users'))
        sm.add_widget(AdminSettingsScreen(name='admin_settings'))
        return sm

    def on_start(self):
        self.db.initialize()

    def on_pause(self):
        return True

    def on_resume(self):
        pass


if __name__ == '__main__':
    QI1489App().run()
