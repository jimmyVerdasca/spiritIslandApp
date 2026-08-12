from kivymd.uix.screen import MDScreen

from kivymd.app import MDApp

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel

from kivy.metrics import dp
from kivy.uix.widget import Widget


class BaseScreen(MDScreen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # --------------------------------------------
        # Navigation
        # --------------------------------------------

        self.previous_screen = "home"


        # --------------------------------------------
        # Managers
        # --------------------------------------------

        app = MDApp.get_running_app()

        self.settings_manager = app.settings_manager
        self.language_manager = app.language_manager
        self.theme_manager = app.theme_manager


        # --------------------------------------------
        # Top bar references
        # --------------------------------------------

        self.top_bar = None
        self.top_bar_title = None
        self.back_button = None
        self.settings_button = None


        # Translation key used by the top bar
        self.top_bar_title_key = None


    # ====================================================
    # Screen lifecycle
    # ====================================================

    def on_pre_enter(self):

        self.refresh_base_ui()


    # ====================================================
    # Add top bar
    # ====================================================

    def add_top_bar(
        self,
        layout,
        title_key,
    ):

        self.top_bar_title_key = title_key


        # --------------------------------------------
        # Top bar
        # --------------------------------------------

        self.top_bar = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(56),
            spacing=dp(8),
            padding=[
                dp(5),
                dp(4),
            ],
        )


        # --------------------------------------------
        # Back button
        # --------------------------------------------

        self.back_button = MDIconButton(
            icon="arrow-left",
            icon_size=dp(26),
            size_hint=(None, None),
            size=(dp(48), dp(48)),
        )

        self.back_button.bind(
            on_release=self.go_back,
        )


        # --------------------------------------------
        # Title
        # --------------------------------------------

        self.top_bar_title = MDLabel(
            font_style="H5",
            valign="center",
            size_hint_x=None,
        )


        # Allow title to take available space

        self.top_bar_title.size_hint_x = 1


        # --------------------------------------------
        # Settings button
        # --------------------------------------------

        self.settings_button = MDIconButton(
            icon="cog-outline",
            icon_size=dp(26),
            size_hint=(None, None),
            size=(dp(48), dp(48)),
        )

        self.settings_button.bind(
            on_release=lambda instance:
            self.navigate_to("settings")
        )


        # --------------------------------------------
        # Build bar
        # --------------------------------------------

        self.top_bar.add_widget(
            self.back_button
        )

        self.top_bar.add_widget(
            self.top_bar_title
        )

        self.top_bar.add_widget(
            Widget()
        )

        self.top_bar.add_widget(
            self.settings_button
        )


        layout.add_widget(
            self.top_bar
        )


        # --------------------------------------------
        # Apply initial appearance
        # --------------------------------------------

        self.refresh_base_ui()


    # ====================================================
    # Refresh base UI
    # ====================================================

    def refresh_base_ui(self):

        if not self.top_bar_title:

            return


        self.update_top_bar_text()

        self.update_top_bar_theme()


    # ====================================================
    # Translation
    # ====================================================

    def update_top_bar_text(self):

        if not self.top_bar_title_key:

            return


        self.top_bar_title.text = (
            self.language_manager.get(
                self.top_bar_title_key
            )
        )


    # ====================================================
    # Theme
    # ====================================================

    def update_top_bar_theme(self):

        text_primary = (
            self.theme_manager.get(
                "text_primary"
            )
        )

        icon = (
            self.theme_manager.get(
                "icon"
            )
        )

        button_color = self.theme_manager.get(
            "top_bar_button"
        )


        # --------------------------------------------
        # Title
        # --------------------------------------------

        self.top_bar_title.theme_text_color = (
            "Custom"
        )

        self.top_bar_title.text_color = (
            text_primary
        )


        # --------------------------------------------
        # Back button
        # --------------------------------------------

        self.back_button.theme_icon_color = (
            "Custom"
        )

        self.back_button.icon_color = (
            icon
        )

        self.back_button.md_bg_color = (
            button_color
        )


        # --------------------------------------------
        # Settings button
        # --------------------------------------------

        self.settings_button.theme_icon_color = (
            "Custom"
        )

        self.settings_button.icon_color = (
            icon
        )

        self.settings_button.md_bg_color = (
            button_color
        )


    # ====================================================
    # Back navigation
    # ====================================================

    def go_back(self, instance):

        if not self.previous_screen:
            return


        previous = self.previous_screen

        self.previous_screen = None

        self.manager.current = previous


    # ====================================================
    # Navigation
    # ====================================================

    def navigate_to(
        self,
        screen_name,
        previous=None,
        **kwargs
    ):

        current = self.manager.current


        # --------------------------------------------
        # Never navigate to the screen we're already on
        # --------------------------------------------

        if current == screen_name:
            return


        screen = self.manager.get_screen(
            screen_name
        )


        # --------------------------------------------
        # Remember where destination came from
        # --------------------------------------------

        if previous is not None:

            screen.previous_screen = previous

        else:

            screen.previous_screen = current


        # --------------------------------------------
        # Pass data
        # --------------------------------------------

        for key, value in kwargs.items():

            setattr(
                screen,
                key,
                value
            )


        # --------------------------------------------
        # Navigate
        # --------------------------------------------

        self.manager.current = screen_name
