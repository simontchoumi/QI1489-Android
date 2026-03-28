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
<AdminUsersScreen>:
    name: 'admin_users'
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
                text: 'Users'
                font_style: 'H6'
                theme_text_color: 'Custom'
                text_color: 1, 1, 1, 1

        MDBoxLayout:
            size_hint_y: None
            height: dp(52)
            padding: dp(8), dp(4)
            spacing: dp(4)

            MDTextField:
                id: search_field
                hint_text: 'Search users...'
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

        MDLabel:
            id: user_count
            text: ''
            font_style: 'Caption'
            theme_text_color: 'Custom'
            text_color: 0.533, 0.569, 0.69, 1
            size_hint_y: None
            height: dp(28)
            padding: dp(12), 0

        ScrollView:
            MDBoxLayout:
                id: user_list
                orientation: 'vertical'
                spacing: dp(6)
                padding: dp(10)
                adaptive_height: True
'''

Builder.load_string(KV)


class AdminUsersScreen(MDScreen):
    def on_enter(self):
        self._load_users()

    def _load_users(self, search=''):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        users = app.db.get_all_users(search=search)
        self.ids.user_count.text = f'  {len(users)} users total'
        lst = self.ids.user_list
        lst.clear_widgets()
        for u in users:
            card = self._make_user_card(u, app.current_user)
            lst.add_widget(card)

    def _make_user_card(self, u, current_user):
        card = MDCard(
            orientation='vertical', padding=dp(12), spacing=dp(6),
            size_hint_y=None, height=dp(100),
            md_bg_color=(0.082, 0.094, 0.204, 1), radius=[dp(10)],
        )
        top = BoxLayout(orientation='horizontal', spacing=dp(6),
                        size_hint_y=None, height=dp(36))

        avatar = MDLabel(
            text=u['username'][0].upper(),
            theme_text_color='Custom', text_color=(0.424, 0.388, 1, 1),
            font_style='H6', size_hint_x=None, width=dp(32), halign='center',
        )
        top.add_widget(avatar)

        info = BoxLayout(orientation='vertical', spacing=dp(2))
        name_lbl = MDLabel(
            text=u['username'],
            theme_text_color='Custom', text_color=(1, 1, 1, 1), font_style='Subtitle2',
        )
        email_lbl = MDLabel(
            text=u['email'],
            theme_text_color='Custom', text_color=(0.533, 0.569, 0.69, 1), font_style='Caption',
        )
        info.add_widget(name_lbl)
        info.add_widget(email_lbl)
        top.add_widget(info)
        card.add_widget(top)

        bottom = BoxLayout(orientation='horizontal', spacing=dp(4),
                           size_hint_y=None, height=dp(38))
        uid = u['id']
        is_self = (current_user and current_user['id'] == uid)

        # Status badge
        status_lbl = MDLabel(
            text='ACTIVE' if u.get('is_active') else 'DISABLED',
            theme_text_color='Custom',
            text_color=(0.024, 0.839, 0.627, 1) if u.get('is_active') else (0.937, 0.278, 0.435, 1),
            font_style='Caption', size_hint_x=None, width=dp(70), halign='center',
        )
        admin_lbl = MDLabel(
            text='ADMIN' if u.get('is_admin') else 'USER',
            theme_text_color='Custom',
            text_color=(1, 0.718, 0.012, 1) if u.get('is_admin') else (0.533, 0.569, 0.69, 1),
            font_style='Caption', size_hint_x=None, width=dp(50), halign='center',
        )
        bottom.add_widget(status_lbl)
        bottom.add_widget(admin_lbl)
        bottom.add_widget(BoxLayout())  # spacer

        if not is_self:
            toggle_active_btn = MDIconButton(
                icon='account-check' if not u.get('is_active') else 'account-off',
                size_hint=None, size=(dp(36), dp(36)),
                theme_icon_color='Custom',
                icon_color=(0.024, 0.839, 0.627, 1),
            )
            toggle_active_btn.bind(on_release=lambda x, i=uid: self.toggle_active(i))
            bottom.add_widget(toggle_active_btn)

            toggle_admin_btn = MDIconButton(
                icon='shield-star' if not u.get('is_admin') else 'shield-off',
                size_hint=None, size=(dp(36), dp(36)),
                theme_icon_color='Custom',
                icon_color=(1, 0.718, 0.012, 1),
            )
            toggle_admin_btn.bind(on_release=lambda x, i=uid: self.toggle_admin(i))
            bottom.add_widget(toggle_admin_btn)

            del_btn = MDIconButton(
                icon='delete', size_hint=None, size=(dp(36), dp(36)),
                theme_icon_color='Custom', icon_color=(0.937, 0.278, 0.435, 1),
            )
            del_btn.bind(on_release=lambda x, i=uid: self.confirm_delete(i))
            bottom.add_widget(del_btn)

        card.add_widget(bottom)
        return card

    def do_search(self):
        self._load_users(search=self.ids.search_field.text.strip())

    def toggle_active(self, uid):
        from kivymd.app import MDApp
        MDApp.get_running_app().db.toggle_user_active(uid)
        self._load_users(self.ids.search_field.text.strip())
        Snackbar(text='User status updated.', snackbar_x='10dp', snackbar_y='10dp',
                 size_hint_x=0.9, bg_color=(0.024, 0.839, 0.627, 1)).open()

    def toggle_admin(self, uid):
        from kivymd.app import MDApp
        MDApp.get_running_app().db.toggle_user_admin(uid)
        self._load_users(self.ids.search_field.text.strip())
        Snackbar(text='Admin rights updated.', snackbar_x='10dp', snackbar_y='10dp',
                 size_hint_x=0.9, bg_color=(1, 0.718, 0.012, 1)).open()

    def confirm_delete(self, uid):
        self._pending_uid = uid
        self._dialog = MDDialog(
            title='Delete User',
            text='Delete this user? Their scores will be anonymized.',
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
        MDApp.get_running_app().db.delete_user(self._pending_uid)
        self._load_users()
        Snackbar(text='User deleted.', snackbar_x='10dp', snackbar_y='10dp',
                 size_hint_x=0.9, bg_color=(0.024, 0.839, 0.627, 1)).open()

    def go_back(self):
        self.manager.current = 'admin_dashboard'
