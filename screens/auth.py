from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel

KV = '''
<LoginScreen>:
    name: 'login'
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
                text: 'Sign In'
                font_style: 'H6'
                theme_text_color: 'Custom'
                text_color: 1, 1, 1, 1

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(16)
                padding: dp(24)
                adaptive_height: True

                Widget:
                    size_hint_y: None
                    height: dp(30)

                MDLabel:
                    text: 'QI[color=#FFB703]1489[/color]'
                    markup: True
                    halign: 'center'
                    font_style: 'H4'
                    theme_text_color: 'Custom'
                    text_color: 0.424, 0.388, 1, 1
                    size_hint_y: None
                    height: dp(50)

                MDLabel:
                    text: 'World Knowledge Quiz'
                    halign: 'center'
                    font_style: 'Caption'
                    theme_text_color: 'Custom'
                    text_color: 0.533, 0.569, 0.69, 1
                    size_hint_y: None
                    height: dp(24)

                Widget:
                    size_hint_y: None
                    height: dp(20)

                MDTextField:
                    id: username_field
                    hint_text: 'Username or Email'
                    icon_right: 'account'
                    mode: 'rectangle'
                    size_hint_y: None
                    height: dp(56)

                MDTextField:
                    id: password_field
                    hint_text: 'Password'
                    icon_right: 'eye-off'
                    password: True
                    mode: 'rectangle'
                    size_hint_y: None
                    height: dp(56)

                Widget:
                    size_hint_y: None
                    height: dp(8)

                MDRaisedButton:
                    text: 'Sign In'
                    md_bg_color: 0.424, 0.388, 1, 1
                    size_hint_x: 1
                    height: dp(48)
                    size_hint_y: None
                    on_release: root.do_login()

                MDBoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(40)
                    spacing: dp(4)

                    MDLabel:
                        text: "Don't have an account?"
                        halign: 'right'
                        theme_text_color: 'Custom'
                        text_color: 0.533, 0.569, 0.69, 1
                        font_style: 'Caption'

                    MDFlatButton:
                        text: 'Register'
                        theme_text_color: 'Custom'
                        text_color: 0.424, 0.388, 1, 1
                        on_release: root.go_register()

                MDFlatButton:
                    text: 'Continue as Guest'
                    theme_text_color: 'Custom'
                    text_color: 0.533, 0.569, 0.69, 1
                    size_hint_x: 1
                    height: dp(40)
                    size_hint_y: None
                    on_release: root.go_back()


<RegisterScreen>:
    name: 'register'
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
                text: 'Create Account'
                font_style: 'H6'
                theme_text_color: 'Custom'
                text_color: 1, 1, 1, 1

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(14)
                padding: dp(24)
                adaptive_height: True

                Widget:
                    size_hint_y: None
                    height: dp(20)

                MDTextField:
                    id: reg_username
                    hint_text: 'Username'
                    icon_right: 'account'
                    mode: 'rectangle'
                    size_hint_y: None
                    height: dp(56)

                MDTextField:
                    id: reg_email
                    hint_text: 'Email'
                    icon_right: 'email'
                    mode: 'rectangle'
                    size_hint_y: None
                    height: dp(56)

                MDTextField:
                    id: reg_password
                    hint_text: 'Password'
                    icon_right: 'eye-off'
                    password: True
                    mode: 'rectangle'
                    size_hint_y: None
                    height: dp(56)

                MDTextField:
                    id: reg_confirm
                    hint_text: 'Confirm Password'
                    icon_right: 'eye-off'
                    password: True
                    mode: 'rectangle'
                    size_hint_y: None
                    height: dp(56)

                Widget:
                    size_hint_y: None
                    height: dp(8)

                MDRaisedButton:
                    text: 'Create Account'
                    md_bg_color: 0.424, 0.388, 1, 1
                    size_hint_x: 1
                    height: dp(48)
                    size_hint_y: None
                    on_release: root.do_register()

                MDFlatButton:
                    text: 'Already have an account? Sign In'
                    theme_text_color: 'Custom'
                    text_color: 0.424, 0.388, 1, 1
                    size_hint_x: 1
                    size_hint_y: None
                    height: dp(40)
                    on_release: root.go_login()
'''

Builder.load_string(KV)


def _snack(msg, color=(0.424, 0.388, 1, 1)):
    Snackbar(text=msg, snackbar_x='10dp', snackbar_y='10dp',
             size_hint_x=0.9, bg_color=color).open()


class LoginScreen(MDScreen):
    def do_login(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        username = self.ids.username_field.text.strip()
        password = self.ids.password_field.text
        if not username or not password:
            _snack('Please fill in all fields.', (0.937, 0.278, 0.435, 1))
            return
        user = app.db.authenticate_user(username, password)
        if user:
            app.current_user = user
            self.ids.username_field.text = ''
            self.ids.password_field.text = ''
            _snack(f'Welcome, {user["username"]}!', (0.024, 0.839, 0.627, 1))
            self.manager.current = 'profile'
        else:
            _snack('Invalid credentials.', (0.937, 0.278, 0.435, 1))

    def go_register(self):
        self.manager.current = 'register'

    def go_back(self):
        self.manager.current = 'menu'


class RegisterScreen(MDScreen):
    def do_register(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        username = self.ids.reg_username.text.strip()
        email = self.ids.reg_email.text.strip()
        password = self.ids.reg_password.text
        confirm = self.ids.reg_confirm.text
        if not all([username, email, password, confirm]):
            _snack('Please fill in all fields.', (0.937, 0.278, 0.435, 1))
            return
        if password != confirm:
            _snack('Passwords do not match.', (0.937, 0.278, 0.435, 1))
            return
        if len(password) < 6:
            _snack('Password must be at least 6 characters.', (0.937, 0.278, 0.435, 1))
            return
        ok, msg = app.db.create_user(username, email, password)
        if ok:
            user = app.db.authenticate_user(username, password)
            app.current_user = user
            for fid in ['reg_username', 'reg_email', 'reg_password', 'reg_confirm']:
                self.ids[fid].text = ''
            _snack('Account created!', (0.024, 0.839, 0.627, 1))
            self.manager.current = 'profile'
        else:
            _snack(msg, (0.937, 0.278, 0.435, 1))

    def go_login(self):
        self.manager.current = 'login'

    def go_back(self):
        self.manager.current = 'login'
