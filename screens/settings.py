from .baseScreen import BaseScreen

from kivy.metrics import dp

from kivymd.app import MDApp

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDRaisedButton


class SettingsScreen(BaseScreen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # =================================================
        # Managers
        # =================================================

        app = MDApp.get_running_app()

        self.settings_manager = app.settings_manager
        self.language_manager = app.language_manager
        self.theme_manager = app.theme_manager

        # =================================================
        # Main layout
        # =================================================

        self.layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(20),
        )

        self.add_widget(self.layout)

        # =================================================
        # Build screen
        # =================================================

        self.build_screen()

    # =================================================
    # Lifecycle
    # =================================================

    def on_pre_enter(self):

        super().on_pre_enter()

        self.refresh_ui()

    # =================================================
    # Build screen
    # =================================================

    def build_screen(self):

        self.layout.clear_widgets()

        # ---------------------------------------------
        # Top bar
        # ---------------------------------------------

        self.add_top_bar(
            self.layout,
            "settings"
        )

        # ---------------------------------------------
        # Scroll area
        # ---------------------------------------------

        scroll = MDScrollView()

        self.container = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            adaptive_height=True,
        )

        scroll.add_widget(
            self.container
        )

        self.layout.add_widget(
            scroll
        )

        # ---------------------------------------------
        # Settings
        # ---------------------------------------------

        self.build_settings()

    # =================================================
    # Build settings
    # =================================================

    def build_settings(self):

        self.container.clear_widgets()

        # =================================================
        # LANGUAGE
        # =================================================

        language_card = MDCard(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10),
            size_hint_y=None,
            height=dp(130),
            style="outlined",
            line_width=dp(1),
        )

        language_title = MDLabel(
            text=self.language_manager.get(
                "language"
            ),
            bold=True,
            adaptive_height=True,
        )

        self.apply_label_theme(
            language_title,
            "text_primary"
        )

        language_description = MDLabel(
            text=self.language_manager.get(
                "language_description"
            ),
            adaptive_height=True,
        )

        self.apply_label_theme(
            language_description,
            "text_secondary"
        )

        language_buttons = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(45),
        )

        self.en_button = MDRaisedButton(
            text="English",
            on_release=lambda x:
                self.set_language("en"),
        )

        self.fr_button = MDRaisedButton(
            text="Français",
            on_release=lambda x:
                self.set_language("fr"),
        )

        language_buttons.add_widget(
            self.en_button
        )

        language_buttons.add_widget(
            self.fr_button
        )

        language_card.add_widget(
            language_title
        )

        language_card.add_widget(
            language_description
        )

        language_card.add_widget(
            language_buttons
        )

        self.container.add_widget(
            language_card
        )

        # =================================================
        # APPEARANCE
        # =================================================

        appearance_card = MDCard(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10),
            size_hint_y=None,
            height=dp(130),
            style="outlined",
            line_width=dp(1),
        )

        appearance_title = MDLabel(
            text=self.language_manager.get(
                "appearance"
            ),
            bold=True,
            adaptive_height=True,
        )

        self.apply_label_theme(
            appearance_title,
            "text_primary"
        )

        appearance_description = MDLabel(
            text=self.language_manager.get(
                "appearance_description"
            ),
            adaptive_height=True,
        )

        self.apply_label_theme(
            appearance_description,
            "text_secondary"
        )

        appearance_buttons = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(45),
        )

        self.light_button = MDRaisedButton(
            text=self.language_manager.get(
                "light"
            ),
            on_release=lambda x:
                self.set_theme("light"),
        )

        self.dark_button = MDRaisedButton(
            text=self.language_manager.get(
                "dark"
            ),
            on_release=lambda x:
                self.set_theme("dark"),
        )

        appearance_buttons.add_widget(
            self.light_button
        )

        appearance_buttons.add_widget(
            self.dark_button
        )

        appearance_card.add_widget(
            appearance_title
        )

        appearance_card.add_widget(
            appearance_description
        )

        appearance_card.add_widget(
            appearance_buttons
        )

        self.container.add_widget(
            appearance_card
        )

        # =================================================
        # Apply theme
        # =================================================

        self.update_theme()

        self.update_button_colors()

    # =================================================
    # UI refresh
    # =================================================

    def refresh_ui(self):

        self.build_screen()

    # =================================================
    # Language
    # =================================================

    def set_language(self, language):

        # ---------------------------------------------
        # Update language manager
        # ---------------------------------------------

        self.language_manager.set_language(
            language
        )

        # ---------------------------------------------
        # Persist setting
        # ---------------------------------------------

        self.settings_manager.set(
            "language",
            language
        )

        # ---------------------------------------------
        # Rebuild screen
        # ---------------------------------------------

        self.build_screen()

        # ---------------------------------------------
        # Notify BaseScreen / top bar
        # ---------------------------------------------

        if hasattr(
            self,
            "update_top_bar"
        ):
            self.update_top_bar()

    # =================================================
    # Theme
    # =================================================

    def set_theme(self, theme):

        # ---------------------------------------------
        # Update theme manager
        # ---------------------------------------------

        self.theme_manager.set_theme(
            theme
        )

        # ---------------------------------------------
        # Persist setting
        # ---------------------------------------------

        self.settings_manager.set(
            "theme",
            theme
        )

        # ---------------------------------------------
        # Apply KivyMD theme
        # ---------------------------------------------

        app = MDApp.get_running_app()

        if theme == "dark":

            app.theme_cls.theme_style = "Dark"

        else:

            app.theme_cls.theme_style = "Light"

        # ---------------------------------------------
        # Rebuild / refresh UI
        # ---------------------------------------------

        self.build_screen()

    # =================================================
    # Theme
    # =================================================

    def update_theme(self):

        self.layout.md_bg_color = (
            self.theme_manager.get(
                "background"
            )
        )

    # =================================================
    # Button colors
    # =================================================

    def update_button_colors(self):

        selected = (
            0,
            0.6,
            0,
            1,
        )

        normal = (
            0.7,
            0.7,
            0.7,
            1,
        )

        # ---------------------------------------------
        # Language
        # ---------------------------------------------

        self.en_button.md_bg_color = normal
        self.fr_button.md_bg_color = normal

        if (
            self.language_manager.current_language
            == "en"
        ):

            self.en_button.md_bg_color = selected

        else:

            self.fr_button.md_bg_color = selected

        # ---------------------------------------------
        # Theme
        # ---------------------------------------------

        self.light_button.md_bg_color = normal
        self.dark_button.md_bg_color = normal

        if (
            self.theme_manager.current_theme
            == "light"
        ):

            self.light_button.md_bg_color = selected

        else:

            self.dark_button.md_bg_color = selected

    # =================================================
    # Label theme helper
    # =================================================

    def apply_label_theme(
        self,
        label,
        theme_key,
    ):

        label.theme_text_color = "Custom"

        label.text_color = (
            self.theme_manager.get(
                theme_key
            )
        )