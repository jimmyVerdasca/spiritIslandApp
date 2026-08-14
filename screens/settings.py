from .baseScreen import BaseScreen

from kivymd.app import MDApp

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView


class SettingsScreen(BaseScreen):

    """
    Application settings screen.

    Responsibilities:

        - Display language settings.
        - Display appearance settings.
        - Change and persist application settings.

    Shared widget creation, theme values, dimensions,
    typography, and top-bar behavior are provided by
    BaseScreen / WidgetFactory.
    """

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

            spacing=self.spacing(
                "sm"
            ),

            padding=self.dimension(
                "screen",
                "padding",
            ),
        )

        self.add_widget(
            self.layout
        )

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
            "settings",
        )

        # ---------------------------------------------
        # Scroll area
        # ---------------------------------------------

        scroll = MDScrollView()

        self.container = MDBoxLayout(

            orientation="vertical",

            spacing=self.spacing(
                "sm"
            ),

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
        self.update_button_colors()

    # =================================================
    # Build settings
    # =================================================

    def build_settings(self):

        self.container.clear_widgets()

        self.build_language_section()

        self.build_appearance_section()

    # =================================================
    # Language
    # =================================================

    def build_language_section(self):

        card = self.create_card(

            orientation="vertical",

            adaptive_height=True,

            padding=self.dimension(
                "card",
                "padding",
            ),

            spacing=self.spacing(
                "sm"
            ),
        )

        title = self.create_label(

            text=str(
                self.language_manager.get(
                    "language"
                )
            ),

            style="subtitle",

            color="text_primary",

            size_hint_y=None,
        )

        title.bold = True

        title.bind(
            texture_size=lambda instance, value:
            setattr(
                instance,
                "height",
                value[1],
            )
        )

        description = self.create_label(

            text=str(
                self.language_manager.get(
                    "language_description"
                )
            ),

            style="secondary",

            color="text_secondary",

            size_hint_y=None,
        )

        description.bind(
            texture_size=lambda instance, value:
            setattr(
                instance,
                "height",
                value[1],
            )
        )

        buttons = MDBoxLayout(

            orientation="horizontal",

            spacing=self.spacing(
                "sm"
            ),

            size_hint_y=None,

            height=self.dimension(
                "button",
                "height",
            ),
        )

        self.en_button = self.create_button(

            text="English",

            background_color="inactive_button",

            text_color="text_primary",

            on_release=lambda instance:
            self.set_language("en"),
        )

        self.fr_button = self.create_button(

            text="Français",

            background_color="inactive_button",

            text_color="text_primary",

            on_release=lambda instance:
            self.set_language("fr"),
        )

        buttons.add_widget(
            self.en_button
        )

        buttons.add_widget(
            self.fr_button
        )

        card.add_widget(
            title
        )

        card.add_widget(
            description
        )

        card.add_widget(
            buttons
        )

        self.container.add_widget(
            card
        )

    # =================================================
    # Appearance
    # =================================================

    def build_appearance_section(self):

        card = self.create_card(

            orientation="vertical",

            adaptive_height=True,

            padding=self.dimension(
                "card",
                "padding",
            ),

            spacing=self.spacing(
                "sm"
            ),
        )

        title = self.create_label(

            text=str(
                self.language_manager.get(
                    "appearance"
                )
            ),

            style="subtitle",

            color="text_primary",

            size_hint_y=None,
        )

        title.bold = True

        title.bind(
            texture_size=lambda instance, value:
            setattr(
                instance,
                "height",
                value[1],
            )
        )

        description = self.create_label(

            text=str(
                self.language_manager.get(
                    "appearance_description"
                )
            ),

            style="secondary",

            color="text_secondary",

            size_hint_y=None,
        )

        description.bind(
            texture_size=lambda instance, value:
            setattr(
                instance,
                "height",
                value[1],
            )
        )

        buttons = MDBoxLayout(

            orientation="horizontal",

            spacing=self.spacing(
                "sm"
            ),

            size_hint_y=None,

            height=self.dimension(
                "button",
                "height",
            ),
        )

        self.light_button = self.create_button(

            text=str(
                self.language_manager.get(
                    "light"
                )
            ),

            background_color="inactive_button",

            text_color="text_primary",

            on_release=lambda instance:
            self.set_theme("light"),
        )

        self.dark_button = self.create_button(

            text=str(
                self.language_manager.get(
                    "dark"
                )
            ),

            background_color="inactive_button",

            text_color="text_primary",

            on_release=lambda instance:
            self.set_theme("dark"),
        )

        buttons.add_widget(
            self.light_button
        )

        buttons.add_widget(
            self.dark_button
        )

        card.add_widget(
            title
        )

        card.add_widget(
            description
        )

        card.add_widget(
            buttons
        )

        self.container.add_widget(
            card
        )

    # =================================================
    # UI refresh
    # =================================================

    def refresh_ui(self):

        self.build_screen()

    # =================================================
    # Language
    # =================================================

    def set_language(
        self,
        language,
    ):

        if language not in (
            "en",
            "fr",
        ):
            return

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
        # Rebuild UI
        # ---------------------------------------------

        self.build_screen()

        # ---------------------------------------------
        # Refresh top bar
        # ---------------------------------------------

        if hasattr(
            self,
            "update_top_bar",
        ):

            self.update_top_bar()

    # =================================================
    # Theme
    # =================================================

    def set_theme(
        self,
        theme,
    ):

        if theme not in (
            "light",
            "dark",
        ):
            return

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
        # Apply KivyMD global theme
        # ---------------------------------------------

        app = MDApp.get_running_app()

        app.theme_cls.theme_style = (
            "Dark"
            if theme == "dark"
            else "Light"
        )

        # ---------------------------------------------
        # Rebuild UI
        # ---------------------------------------------

        self.build_screen()

    def update_button_colors(self):
    
        buttons = (
            self.en_button,
            self.fr_button,
            self.light_button,
            self.dark_button,
        )

        for button in buttons:

            self.apply_button_theme(
                button,
                background_color="inactive_button",
                text_color="text_primary",
            )

        if self.language_manager.current_language == "en":

            self.apply_button_theme(
                self.en_button,
                background_color="button",
                text_color="text_primary",
            )

        else:

            self.apply_button_theme(
                self.fr_button,
                background_color="button",
                text_color="text_primary",
            )

        if self.theme_manager.current_theme == "light":

            self.apply_button_theme(
                self.light_button,
                background_color="button",
                text_color="text_primary",
            )

        else:

            self.apply_button_theme(
                self.dark_button,
                background_color="button",
                text_color="text_primary",
            )