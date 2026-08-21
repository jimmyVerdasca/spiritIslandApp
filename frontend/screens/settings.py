# ============================================================
# screens/settings.py
# ============================================================

from kivymd.app import MDApp

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView

from .baseScreen import BaseScreen


class SettingsScreen(BaseScreen):

    """
    Application settings screen.

    Handles:

        - Language
        - Light / dark appearance
        - Color theme / palette file
        - Persistence of settings
    """

    THEME_FILE_LABELS = {

        "themes":
            "Original",

        "sunset_ocean":
            "Sunset Ocean",

        "sunset_coral":
            "Sunset Coral",

        "deep_teal":
            "Deep Teal",

        "tropical_earth":
            "Tropical Earth",

        "forest_island":
            "Forest Island",
    }

    def __init__(
        self,
        **kwargs,
    ):

        super().__init__(
            **kwargs
        )

        # ====================================================
        # Managers
        # ====================================================

        app = MDApp.get_running_app()

        self.settings_manager = (
            app.settings_manager
        )

        self.language_manager = (
            app.language_manager
        )

        self.theme_manager = (
            app.theme_manager
        )

        # ====================================================
        # Main layout
        # ====================================================

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

        # ====================================================
        # Build
        # ====================================================

        self.build_screen()

    # ========================================================
    # Lifecycle
    # ========================================================

    def on_pre_enter(self):

        super().on_pre_enter()

        self.refresh_ui()

    # ========================================================
    # Build screen
    # ========================================================

    def build_screen(self):

        self.layout.clear_widgets()

        # ----------------------------------------------------
        # Top bar
        # ----------------------------------------------------

        self.add_top_bar(
            self.layout,
            "settings",
        )

        # ----------------------------------------------------
        # Scroll area
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # Settings sections
        # ----------------------------------------------------

        self.build_settings()

        self.update_button_colors()

    # ========================================================
    # Build settings
    # ========================================================

    def build_settings(self):

        self.container.clear_widgets()

        self.build_language_section()

        self.build_appearance_section()

        self.build_theme_file_section()

    # ========================================================
    # Language
    # ========================================================

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
            self.set_language(
                "en"
            ),
        )

        self.fr_button = self.create_button(

            text="Français",

            background_color="inactive_button",

            text_color="text_primary",

            on_release=lambda instance:
            self.set_language(
                "fr"
            ),
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

    # ========================================================
    # Appearance
    # ========================================================

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
            self.set_theme(
                "light"
            ),
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
            self.set_theme(
                "dark"
            ),
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

    # ========================================================
    # Theme file / color palette
    # ========================================================

    def build_theme_file_section(self):

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

        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

        title = self.create_label(

            text="Color theme",

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

        # ----------------------------------------------------
        # Description
        # ----------------------------------------------------

        description = self.create_label(

            text=(
                "Choose the color palette used by "
                "the application."
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

        # ----------------------------------------------------
        # Theme files
        # ----------------------------------------------------

        theme_files = (
            self.theme_manager.available_theme_files()
        )

        columns = 2

        rows = (
            (
                len(theme_files)
                + columns
                - 1
            )
            // columns
        )

        button_height = self.dimension(
            "button",
            "height",
        )

        spacing = self.spacing(
            "sm"
        )

        buttons = MDGridLayout(

            cols=columns,

            rows=rows,

            spacing=spacing,

            size_hint_y=None,

            height=(
                rows
                * button_height
                +
                max(
                    0,
                    rows - 1,
                )
                * spacing
            ),
        )

        self.theme_file_buttons = {}

        for theme_file in theme_files:

            label = (
                self.THEME_FILE_LABELS.get(
                    theme_file,
                    theme_file.replace(
                        "_",
                        " ",
                    ).title(),
                )
            )

            button = self.create_button(

                text=label,

                background_color="inactive_button",

                text_color="text_primary",

                on_release=lambda instance,
                selected_theme_file=theme_file:
                self.set_theme_file(
                    selected_theme_file
                ),
            )

            self.theme_file_buttons[
                theme_file
            ] = button

            buttons.add_widget(
                button
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

    # ========================================================
    # UI refresh
    # ========================================================

    def refresh_ui(self):

        self.build_screen()

    # ========================================================
    # Language
    # ========================================================

    def set_language(
        self,
        language,
    ):

        if language not in (
            "en",
            "fr",
        ):

            return

        # ----------------------------------------------------
        # Manager
        # ----------------------------------------------------

        self.language_manager.set_language(
            language
        )

        # ----------------------------------------------------
        # Persistence
        # ----------------------------------------------------

        self.settings_manager.set(
            "language",
            language,
        )

        # ----------------------------------------------------
        # Rebuild
        # ----------------------------------------------------

        self.build_screen()

    # ========================================================
    # Theme
    # ========================================================

    def set_theme(
        self,
        theme,
    ):

        if theme not in (
            "light",
            "dark",
        ):

            return

        # ----------------------------------------------------
        # Manager
        # ----------------------------------------------------

        self.theme_manager.set_theme(
            theme
        )

        # ----------------------------------------------------
        # Persistence
        # ----------------------------------------------------

        self.settings_manager.set(
            "theme",
            theme,
        )

        # ----------------------------------------------------
        # KivyMD
        # ----------------------------------------------------

        self._sync_kivymd_theme()

        # ----------------------------------------------------
        # Rebuild
        # ----------------------------------------------------

        self.build_screen()

    # ========================================================
    # Theme file
    # ========================================================

    def set_theme_file(
        self,
        theme_file,
    ):

        if (
            theme_file
            not in self.theme_manager.available_theme_files()
        ):

            return

        # ----------------------------------------------------
        # Save current theme before changing palette.
        # ----------------------------------------------------

        previous_theme = (
            self.theme_manager.current_theme
        )

        # ----------------------------------------------------
        # Load
        # ----------------------------------------------------

        try:

            self.theme_manager.load_theme_file(
                theme_file
            )

        except (
            ImportError,
            ValueError,
            KeyError,
        ) as error:

            print(
                f"Failed to load theme file "
                f"'{theme_file}': {error}"
            )

            return

        # ----------------------------------------------------
        # Persistence
        # ----------------------------------------------------

        self.settings_manager.set(
            "theme_file",
            theme_file,
        )

        # If the new palette still supports the old theme,
        # keep it. ThemeManager already does this, but this
        # makes the intention explicit.
        if (
            previous_theme
            in self.theme_manager.available_themes()
        ):

            if (
                self.theme_manager.current_theme
                != previous_theme
            ):

                self.theme_manager.set_theme(
                    previous_theme
                )

        # Persist the actual theme selected by the new file.
        self.settings_manager.set(
            "theme",
            self.theme_manager.current_theme,
        )

        # ----------------------------------------------------
        # KivyMD
        # ----------------------------------------------------

        self._sync_kivymd_theme()

        # ----------------------------------------------------
        # Rebuild
        # ----------------------------------------------------

        self.build_screen()

    # ========================================================
    # KivyMD synchronization
    # ========================================================

    def _sync_kivymd_theme(self):

        app = MDApp.get_running_app()

        if (
            self.theme_manager.current_theme
            == "dark"
        ):

            app.theme_cls.theme_style = "Dark"

        else:

            app.theme_cls.theme_style = "Light"

    # ========================================================
    # Button colors
    # ========================================================

    def update_button_colors(self):

        buttons = (
            self.en_button,
            self.fr_button,
            self.light_button,
            self.dark_button,
        )

        # ----------------------------------------------------
        # Reset language/appearance buttons
        # ----------------------------------------------------

        for button in buttons:

            self.apply_button_theme(
                button,
                background_color="inactive_button",
                text_color="text_primary",
            )

        # ----------------------------------------------------
        # Selected language
        # ----------------------------------------------------

        if (
            self.language_manager.current_language
            == "en"
        ):

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

        # ----------------------------------------------------
        # Selected appearance
        # ----------------------------------------------------

        if (
            self.theme_manager.current_theme
            == "light"
        ):

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

        # ----------------------------------------------------
        # Selected color theme
        # ----------------------------------------------------

        if not hasattr(
            self,
            "theme_file_buttons",
        ):

            return

        for (
            theme_file,
            button,
        ) in self.theme_file_buttons.items():

            self.apply_button_theme(
                button,
                background_color="inactive_button",
                text_color="text_primary",
            )

            if (
                theme_file
                == self.theme_manager.current_theme_file
            ):

                self.apply_button_theme(
                    button,
                    background_color="button",
                    text_color="text_primary",
                )

    # ========================================================
    # Screen-specific theme refresh
    # ========================================================

    def refresh_screen_theme(self):

        """
        Refresh settings-specific widgets when a theme
        changes without requiring the entire application
        to restart.
        """

        if hasattr(
            self,
            "en_button",
        ):

            self.update_button_colors()