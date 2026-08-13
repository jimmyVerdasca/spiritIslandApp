from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from kivy.metrics import dp, sp
from kivy.uix.widget import Widget


class BaseScreen(MDScreen):

    """
    Base class for all application screens.

    Responsibilities:

        - Provide access to application managers.
        - Provide shared design-token helpers.
        - Provide reusable widget factories.
        - Build and theme the common top bar.
        - Handle screen navigation.
        - Refresh common UI when entering a screen.

    Individual screens should focus on:

        - Layout
        - Content
        - Navigation
        - Screen-specific behavior
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # ====================================================
        # Navigation
        # ====================================================

        self.previous_screen = "home"


        # ====================================================
        # Managers
        # ====================================================

        app = MDApp.get_running_app()

        self.settings_manager = app.settings_manager
        self.language_manager = app.language_manager
        self.theme_manager = app.theme_manager


        # ====================================================
        # Top bar
        # ====================================================

        self.top_bar = None
        self.top_bar_title = None
        self.back_button = None
        self.settings_button = None
        self.top_bar_title_key = None

        self.theme_manager.bind_theme_change(self.on_theme_changed)

        # ====================================================
        # Background
        # ====================================================

        self.background_overlay = MDBoxLayout(
            size_hint=(1, 1),
            pos_hint={
                "x": 0,
                "y": 0,
            },

            md_bg_color=self.theme_manager.get(
                "background_overlay"
            ),
        )

        self.add_widget(
            self.background_overlay
        )

    def update_background_theme(self):
        
            background = self.theme_manager.get(
                "background_overlay"
            )
    
            if background is not None:
                self.background_overlay.md_bg_color = background



    # ====================================================
    # Lifecycle
    # ====================================================

    def on_theme_changed(
        self,
        theme
    ):

        self.refresh_base_theme()

        self.refresh_screen_theme()

    def refresh_base_theme(self):
    
        self.refresh_label_themes()
        self.update_top_bar_theme()
        self.update_background_theme()

    def on_pre_enter(self):

        super().on_pre_enter()

        self.refresh_base_ui()


    # ====================================================
    # Design tokens
    # ====================================================

    def spacing(self, size):

        value = self.theme_manager.spacing(
            size
        )

        if value is None:
            return 0

        return dp(value)


    def dimension(self, component, key):

        value = self.theme_manager.get_component(
            component,
            key,
        )

        if value is None:
            return 0

        return dp(value)


    def icon_size(self, size):

        value = self.theme_manager.icon_size(
            size
        )

        if value is None:
            return 0

        return dp(value)


    def font_size(self, style):
    
        value = self.theme_manager.font_size(style)

        if value is None:
            return 0

        return sp(value)


    def line_height(self, style):

        return self.theme_manager.line_height(
            style
        )


    # ====================================================
    # Label factory
    # ====================================================

    def create_label(
        self,
        text="",
        style="body",
        color="text_primary",
        halign="left",
        valign="middle",
        size_hint_y=None,
        **kwargs
    ):

        """
        Create a standard application label.

        Typography and colors are controlled by the
        application's design system.
        """

        label = MDLabel(
            text=str(text),

            halign=halign,
            valign=valign,

            size_hint_y=size_hint_y,

            theme_text_color="Custom",

            **kwargs
        )

        # ------------------------------------------------
        # Store design tokens
        # ------------------------------------------------

        label.app_style = style
        label.app_color = color

        # ------------------------------------------------
        # Typography
        # ------------------------------------------------

        label.font_size = self.font_size(
            style
        )

        # ------------------------------------------------
        # Initial theme color
        # ------------------------------------------------

        text_color = self.theme_manager.get(
            color
        )

        if text_color is not None:

            label.text_color = text_color

        return label


    # ====================================================
    # Card factory
    # ====================================================

    def create_card(
        self,
        **kwargs
    ):

        """
        Create a standard application card.

        Card dimensions are controlled centrally by THEME:

            card.height
            card.padding
            card.spacing
            card.radius

        Do not duplicate these values in individual screens.

        Screen-specific properties can still be supplied
        through kwargs.
        """

        card_height = self.dimension(
            "card",
            "height",
        )

        card_padding = self.dimension(
            "card",
            "padding",
        )

        card_spacing = self.dimension(
            "card",
            "spacing",
        )

        card_radius = self.dimension(
            "card",
            "radius",
        )


        # ------------------------------------------------
        # Shared defaults
        # ------------------------------------------------

        defaults = {

            "size_hint_y": None,

            "height": card_height,

            "padding": card_padding,

            "spacing": card_spacing,

            "radius": [
                card_radius
            ],

            "elevation": 3,
        }


        # ------------------------------------------------
        # Allow explicit screen overrides
        # ------------------------------------------------

        defaults.update(kwargs)


        return MDCard(
            **defaults
        )


    # ====================================================
    # Icon button factory
    # ====================================================

    def create_icon_button(
        self,
        icon,
        size="medium",
        background_color="top_bar_button",
        icon_color="icon",
        **kwargs
    ):

        """
        Create a standard application icon button.

        Button dimensions come from THEME.
        """

        button_size = self.dimension(
            "button",
            "height",
        )


        button = MDIconButton(
            icon=icon,

            icon_size=self.icon_size(
                size
            ),

            size_hint=(None, None),

            size=(
                button_size,
                button_size,
            ),

            theme_icon_color="Custom",

            **kwargs
        )


        # ------------------------------------------------
        # Icon color
        # ------------------------------------------------

        color = self.theme_manager.get(
            icon_color
        )

        if color is not None:

            button.icon_color = color


        # ------------------------------------------------
        # Background color
        # ------------------------------------------------

        if background_color:

            background = (
                self.theme_manager.get(
                    background_color
                )
            )

            if background is not None:

                button.md_bg_color = (
                    background
                )


        return button


    # ====================================================
    # Card text layout
    # ====================================================

    def create_card_text_layout(
        self,
        **kwargs
    ):

        """
        Create the text container used inside cards.

        The important part here is that the container
        does NOT inherit arbitrary vertical spacing.

        Card title and description should sit close together.
        """

        defaults = {

            "orientation": "vertical",

            "spacing": self.spacing(
                "xs"
            ),

            "size_hint_y": 1,

        }

        defaults.update(kwargs)

        return MDBoxLayout(
            **defaults
        )


    # ====================================================
    # Card title
    # ====================================================

    def create_card_title(
        self,
        text="",
        color="text_primary",
        **kwargs
    ):

        """
        Standard card title.

        The label is vertically centered by the card's
        text container instead of being given a large
        artificial fixed height.
        """

        defaults = {

            "text": text,

            "style": "subtitle",

            "color": color,

            "size_hint_y": 1,

            "valign": "bottom",

        }

        defaults.update(kwargs)

        return self.create_label(
            **defaults
        )


    # ====================================================
    # Card description
    # ====================================================

    def create_card_description(
        self,
        text="",
        color="card_text_secondary",
        **kwargs
    ):

        """
        Standard card description.
        """

        defaults = {

            "text": text,

            "style": "secondary",

            "color": color,

            "size_hint_y": 1,

            "valign": "top",

        }

        defaults.update(kwargs)

        return self.create_label(
            **defaults
        )


    # ====================================================
    # Top bar
    # ====================================================

    def add_top_bar(
        self,
        layout,
        title_key,
    ):

        self.top_bar_title_key = title_key


        # ------------------------------------------------
        # Dimensions
        # ------------------------------------------------

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


        # ------------------------------------------------
        # Top bar
        # ------------------------------------------------

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


        # ------------------------------------------------
        # Back button
        # ------------------------------------------------

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


        # ------------------------------------------------
        # Title
        # ------------------------------------------------

        self.top_bar_title = self.create_label(

            style="title",

            color="text_primary",

            halign="left",

            valign="center",

            size_hint_x=1,

            size_hint_y=1,
        )


        # ------------------------------------------------
        # Settings button
        # ------------------------------------------------

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
            self.navigate_to("settings")
        )


        # ------------------------------------------------
        # Build
        # ------------------------------------------------

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


        self.refresh_base_ui()


    # ====================================================
    # Base UI refresh
    # ====================================================

    def refresh_base_ui(self):

        if self.top_bar_title is None:
            return

        self.update_top_bar_text()
        self.update_top_bar_theme()


    # ====================================================
    # Top bar translation
    # ====================================================

    def update_top_bar_text(self):

        if not self.top_bar_title_key:
            return


        value = self.language_manager.get(
            self.top_bar_title_key
        )


        if isinstance(value, dict):

            title_key = (
                f"{self.top_bar_title_key}_title"
            )

            title_value = (
                self.language_manager.get(
                    title_key
                )
            )

            if (
                isinstance(title_value, str)
                and title_value
            ):

                self.top_bar_title.text = (
                    title_value
                )

            else:

                self.top_bar_title.text = ""

            return


        if value is None:

            self.top_bar_title.text = ""

            return


        self.top_bar_title.text = str(
            value
        )


    # ====================================================
    # Top bar theme
    # ====================================================

    def update_top_bar_theme(self):

        if (
            self.top_bar_title is None
            or self.back_button is None
            or self.settings_button is None
        ):
            return


        text_primary = (
            self.theme_manager.get(
                "text_primary"
            )
        )

        icon_color = (
            self.theme_manager.get(
                "icon"
            )
        )

        button_color = (
            self.theme_manager.get(
                "top_bar_button"
            )
        )


        # ------------------------------------------------
        # Title
        # ------------------------------------------------

        self.top_bar_title.theme_text_color = (
            "Custom"
        )

        if text_primary is not None:

            self.top_bar_title.text_color = (
                text_primary
            )


        # ------------------------------------------------
        # Back button
        # ------------------------------------------------

        self.back_button.theme_icon_color = (
            "Custom"
        )

        if icon_color is not None:

            self.back_button.icon_color = (
                icon_color
            )

        if button_color is not None:

            self.back_button.md_bg_color = (
                button_color
            )


        # ------------------------------------------------
        # Settings button
        # ------------------------------------------------

        self.settings_button.theme_icon_color = (
            "Custom"
        )

        if icon_color is not None:

            self.settings_button.icon_color = (
                icon_color
            )

        if button_color is not None:

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

        if self.manager is None:
            return


        current = self.manager.current


        if current == screen_name:
            return


        screen = self.manager.get_screen(
            screen_name
        )


        if previous is not None:

            screen.previous_screen = previous

        else:

            screen.previous_screen = current


        for key, value in kwargs.items():

            setattr(
                screen,
                key,
                value,
            )


        self.manager.current = (
            screen_name
        )

    def refresh_label_themes(self):

        for widget in self.walk():

            if not isinstance(widget, MDLabel):
                continue

            color_key = getattr(
                widget,
                "app_color",
                None,
            )

            if color_key is not None:

                color = self.theme_manager.get(
                    color_key
                )

                if color is not None:

                    widget.theme_text_color = "Custom"
                    widget.text_color = color


            style = getattr(
                widget,
                "app_style",
                None
            )

            if style is not None:

                widget.font_size = (
                    self.font_size(style)
                )

    def refresh_screen_theme(self):
    
        """
        Override in child screens when the screen has
        theme-specific widgets that need refreshing.
        """

        pass
