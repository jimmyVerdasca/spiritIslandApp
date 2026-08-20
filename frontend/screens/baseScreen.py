# ============================================================
# screens/baseScreen.py
# ============================================================

from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.widget import Widget

from .widgets.theme_helper import ThemeHelper
from .widgets.widget_factory import WidgetFactory


class BaseScreen(MDScreen):

    """
    Common base screen.

    Responsibilities:

        - Application managers
        - Theme access
        - Standardized widget creation
        - Screen navigation
        - Common background
        - Common top bar
        - Screen lifecycle
        - Automatic theme refresh
    """

    def __init__(
        self,
        data,
        **kwargs,
    ):

        super().__init__(
            **kwargs
        )
        
        self.data = data

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
        # Helpers
        # ====================================================

        self.theme = ThemeHelper(
            self.theme_manager
        )

        self.widget_factory = WidgetFactory(
            self.theme
        )

        # ====================================================
        # Navigation
        # ====================================================

        self.previous_screen = "home"

        # ====================================================
        # Top bar
        # ====================================================

        self.top_bar = None
        self.top_bar_title = None
        self.back_button = None
        self.settings_button = None
        self.top_bar_title_key = None

        # ====================================================
        # Theme lifecycle
        # ====================================================

        self.theme_manager.bind_theme_change(
            self.on_theme_changed
        )

        # ====================================================
        # Background
        # ====================================================

        self.background_overlay = MDBoxLayout(

            size_hint=(
                1,
                1,
            ),

            pos_hint={
                "x": 0,
                "y": 0,
            },

            md_bg_color=(
                self.theme_manager.get(
                    "background_overlay",
                    [0, 0, 0, 0],
                )
            ),
        )

        self.add_widget(
            self.background_overlay
        )

    # ========================================================
    # Theme lifecycle
    # ========================================================

    def on_theme_changed(
        self,
        theme,
    ):
        """
        Called automatically whenever the active theme or
        theme file changes.
        """

        self.refresh_base_theme()

        self.refresh_screen_theme()

    def refresh_base_theme(self):

        self.refresh_widget_themes()

        self.update_top_bar_theme()

        self.update_background_theme()

    def refresh_base_ui(self):

        self.update_top_bar_text()

        self.update_top_bar_theme()

        self.update_background_theme()

    # ========================================================
    # Lifecycle
    # ========================================================

    def on_pre_enter(self):

        super().on_pre_enter()

        self.refresh_base_ui()

    # ========================================================
    # Theme helper delegates
    # ========================================================

    def spacing(
        self,
        size,
    ):

        return self.theme.spacing(
            size
        )

    def dimension(
        self,
        component,
        key,
    ):

        return self.theme.dimension(
            component,
            key,
        )

    def font_size(
        self,
        style,
    ):

        return self.theme.font_size(
            style
        )

    def icon_size(
        self,
        size,
    ):

        return self.theme.icon_size(
            size
        )

    # ========================================================
    # Widget factory delegates
    # ========================================================

    def create_label(
        self,
        **kwargs,
    ):

        return self.widget_factory.create_label(
            **kwargs
        )

    def create_card(
        self,
        **kwargs,
    ):

        return self.widget_factory.create_card(
            **kwargs
        )

    def create_icon_button(
        self,
        **kwargs,
    ):

        return self.widget_factory.create_icon_button(
            **kwargs
        )

    def create_button(
        self,
        **kwargs,
    ):

        return self.widget_factory.create_button(
            **kwargs
        )

    def create_card_text_layout(
        self,
        **kwargs,
    ):

        return self.widget_factory.create_card_text_layout(
            **kwargs
        )

    def create_card_title(
        self,
        **kwargs,
    ):

        return self.widget_factory.create_card_title(
            **kwargs
        )

    def create_card_description(
        self,
        **kwargs,
    ):

        return self.widget_factory.create_card_description(
            **kwargs
        )

    def create_input(
        self,
        hint_text="",
        **kwargs,
    ):

        return self.widget_factory.create_input(
            hint_text=hint_text,
            **kwargs,
        )

    def apply_button_theme(
        self,
        button,
        background_color=None,
        text_color=None,
    ):

        self.widget_factory.apply_button_theme(
            button,
            background_color,
            text_color,
        )

    # ========================================================
    # Widget theme refresh
    # ========================================================

    def refresh_widget_themes(self):

        for widget in self.walk():

            # ------------------------------------------------
            # Background
            # ------------------------------------------------

            background_key = getattr(
                widget,
                "app_background_color",
                None,
            )

            if background_key is not None:

                background = (
                    self.theme_manager.get(
                        background_key
                    )
                )

                if background is not None:

                    if hasattr(
                        widget,
                        "md_bg_color",
                    ):

                        widget.md_bg_color = (
                            background
                        )

            # ------------------------------------------------
            # Text
            # ------------------------------------------------

            text_key = getattr(
                widget,
                "app_text_color",
                None,
            )

            if text_key is not None:

                text_color = (
                    self.theme_manager.get(
                        text_key
                    )
                )

                if text_color is not None:

                    if hasattr(
                        widget,
                        "theme_text_color",
                    ):

                        widget.theme_text_color = (
                            "Custom"
                        )

                    if hasattr(
                        widget,
                        "text_color",
                    ):

                        widget.text_color = (
                            text_color
                        )

            # ------------------------------------------------
            # Icon
            # ------------------------------------------------

            icon_key = getattr(
                widget,
                "app_icon_color",
                None,
            )

            if icon_key is not None:

                icon_color = (
                    self.theme_manager.get(
                        icon_key
                    )
                )

                if icon_color is not None:

                    if hasattr(
                        widget,
                        "theme_icon_color",
                    ):

                        widget.theme_icon_color = (
                            "Custom"
                        )

                    if hasattr(
                        widget,
                        "icon_color",
                    ):

                        widget.icon_color = (
                            icon_color
                        )

    # ========================================================
    # Background
    # ========================================================

    def update_background_theme(self):

        if (
            self.background_overlay is None
        ):

            return

        background = (
            self.theme_manager.get(
                "background_overlay"
            )
        )

        if background is not None:

            self.background_overlay.md_bg_color = (
                background
            )

    # ========================================================
    # Top bar
    # ========================================================

    def add_top_bar(
        self,
        layout,
        title_key,
    ):

        self.top_bar_title_key = (
            title_key
        )

        # ====================================================
        # Dimensions
        # ====================================================

        top_bar_height = self.dimension(
            "top_bar",
            "height",
        )

        top_bar_spacing = self.dimension(
            "top_bar",
            "spacing",
        )

        top_bar_padding = self.dimension(
            "top_bar",
            "horizontal_padding",
        )

        # ====================================================
        # Top bar
        # ====================================================

        self.top_bar = MDBoxLayout(

            orientation="horizontal",

            size_hint_y=None,

            height=top_bar_height,

            spacing=top_bar_spacing,

            padding=[
                top_bar_padding,
                0,
                top_bar_padding,
                0,
            ],
        )

        # ====================================================
        # Back button
        # ====================================================

        self.back_button = (
            self.create_icon_button(
                icon="arrow-left",
                size="medium",
                background_color="top_bar_button",
                icon_color="icon",
            )
        )

        self.back_button.bind(
            on_release=self.go_back,
        )

        # ====================================================
        # Title
        # ====================================================

        self.top_bar_title = (
            self.create_label(

                style="title",

                color="text_primary",

                halign="left",

                valign="center",

                size_hint_x=1,

                size_hint_y=1,
            )
        )

        # ====================================================
        # Settings button
        # ====================================================

        self.settings_button = (
            self.create_icon_button(
                icon="cog-outline",
                size="medium",
                background_color="top_bar_button",
                icon_color="icon",
            )
        )

        self.settings_button.bind(
            on_release=lambda instance:
            self.navigate_to(
                "settings"
            )
        )

        # ====================================================
        # Build
        # ====================================================

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

        # ====================================================
        # Initial state
        # ====================================================

        self.refresh_base_ui()

    # ========================================================
    # Top bar translation
    # ========================================================

    def update_top_bar_text(self):

        if self.top_bar_title is None:

            return

        if not self.top_bar_title_key:

            return

        value = (
            self.language_manager.get(
                self.top_bar_title_key
            )
        )

        # ----------------------------------------------------
        # Dictionary translation
        # ----------------------------------------------------

        if isinstance(
            value,
            dict,
        ):

            title_key = (
                f"{self.top_bar_title_key}_title"
            )

            title_value = (
                self.language_manager.get(
                    title_key
                )
            )

            if (
                isinstance(
                    title_value,
                    str,
                )
                and title_value
            ):

                self.top_bar_title.text = (
                    title_value
                )

            else:

                self.top_bar_title.text = ""

            return

        # ----------------------------------------------------
        # Missing translation
        # ----------------------------------------------------

        if value is None:

            self.top_bar_title.text = ""

            return

        # ----------------------------------------------------
        # Normal translation
        # ----------------------------------------------------

        self.top_bar_title.text = str(
            value
        )

    # ========================================================
    # Top bar theme
    # ========================================================

    def update_top_bar_theme(self):

        if self.top_bar_title is None:
            return

        if self.back_button is None:
            return

        if self.settings_button is None:
            return

        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

        text_primary = (
            self.theme_manager.get(
                "text_primary"
            )
        )

        if text_primary is not None:

            if hasattr(
                self.top_bar_title,
                "theme_text_color",
            ):

                self.top_bar_title.theme_text_color = (
                    "Custom"
                )

            if hasattr(
                self.top_bar_title,
                "text_color",
            ):

                self.top_bar_title.text_color = (
                    text_primary
                )

        # ----------------------------------------------------
        # Buttons
        # ----------------------------------------------------

        for button in (
            self.back_button,
            self.settings_button,
        ):

            icon_key = getattr(
                button,
                "app_icon_color",
                "icon",
            )

            background_key = getattr(
                button,
                "app_background_color",
                "top_bar_button",
            )

            icon_color = (
                self.theme_manager.get(
                    icon_key
                )
            )

            background_color = (
                self.theme_manager.get(
                    background_key
                )
            )

            if icon_color is not None:

                if hasattr(
                    button,
                    "theme_icon_color",
                ):

                    button.theme_icon_color = (
                        "Custom"
                    )

                if hasattr(
                    button,
                    "icon_color",
                ):

                    button.icon_color = (
                        icon_color
                    )

            if background_color is not None:

                if hasattr(
                    button,
                    "md_bg_color",
                ):

                    button.md_bg_color = (
                        background_color
                    )

    # ========================================================
    # Navigation
    # ========================================================

    def go_back(
        self,
        instance=None,
    ):

        if not self.previous_screen:

            return

        previous = (
            self.previous_screen
        )

        self.previous_screen = None

        if self.manager is not None:

            self.manager.current = (
                previous
            )

    def navigate_to(
        self,
        screen_name,
        previous=None,
        **kwargs,
    ):

        if self.manager is None:

            return

        current = (
            self.manager.current
        )

        if current == screen_name:

            return

        try:

            screen = (
                self.manager.get_screen(
                    screen_name
                )
            )

        except Exception as error:

            print(
                f"Unable to navigate to "
                f"'{screen_name}': {error}"
            )

            return

        if previous is not None:

            screen.previous_screen = (
                previous
            )

        else:

            screen.previous_screen = (
                current
            )

        for key, value in kwargs.items():

            setattr(
                screen,
                key,
                value,
            )

        self.manager.current = (
            screen_name
        )

    # ========================================================
    # Screen-specific theme
    # ========================================================

    def refresh_screen_theme(self):
        """
        Override in child screens if necessary.
        """

        pass

    # ========================================================
    # Cleanup
    # ========================================================

    def on_leave(self):

        super().on_leave()

        # Do not unbind here.
        #
        # Screens remain alive inside ScreenManager and need
        # to react to future theme changes.