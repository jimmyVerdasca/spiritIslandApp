from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField


class WidgetFactory:

    """
    Creates standardized application widgets.

    Theme values and dimensions are obtained through
    ThemeHelper.

    Widgets store application design tokens as normal
    Python attributes so BaseScreen can refresh them
    when the theme changes.
    """

    def __init__(self, theme):

        self.theme = theme


    # ====================================================
    # Label
    # ====================================================

    def create_label(
        self,
        text="",
        style="body",
        color="text_primary",
        halign="left",
        valign="middle",
        size_hint_y=None,
        **kwargs,
    ):

        label = MDLabel(

            text=str(text),

            halign=halign,
            valign=valign,

            size_hint_y=size_hint_y,

            theme_text_color="Custom",

            **kwargs,
        )


        # ------------------------------------------------
        # Store application design tokens
        # ------------------------------------------------

        label.app_style = style
        label.app_text_color = color


        # ------------------------------------------------
        # Typography
        # ------------------------------------------------

        label.font_size = self.theme.font_size(
            style
        )


        # ------------------------------------------------
        # Initial theme color
        # ------------------------------------------------

        text_color = self.theme.get(
            color
        )

        if text_color is not None:

            label.text_color = text_color


        return label


    # ====================================================
    # Card
    # ====================================================

    def create_card(
        self,
        adaptive_height=False,
        background_color="card",
        **kwargs,
    ):

        defaults = {

            "orientation": "horizontal",

            "padding": self.theme.dimension(
                "card",
                "padding",
            ),

            "spacing": self.theme.dimension(
                "card",
                "spacing",
            ),

            "radius": [
                self.theme.dimension(
                    "card",
                    "radius",
                )
            ],

            "elevation": 3,
        }


        # ------------------------------------------------
        # Height
        # ------------------------------------------------

        if adaptive_height:

            defaults["adaptive_height"] = True

        else:

            defaults["size_hint_y"] = None

            defaults["height"] = (
                self.theme.dimension(
                    "card",
                    "height",
                )
            )


        # ------------------------------------------------
        # Custom KivyMD values
        # ------------------------------------------------

        background = self.theme.get(
            background_color
        )

        if background is not None:

            defaults["md_bg_color"] = background


        # ------------------------------------------------
        # Custom values override defaults
        # ------------------------------------------------

        defaults.update(
            kwargs
        )


        # ------------------------------------------------
        # IMPORTANT:
        #
        # Do NOT put app_background_color in
        # defaults. It is not a Kivy property.
        # ------------------------------------------------

        card = MDCard(
            **defaults
        )


        # ------------------------------------------------
        # Store application design token AFTER creation
        # ------------------------------------------------

        card.app_background_color = (
            background_color
        )


        return card


    # ====================================================
    # Icon button
    # ====================================================

    def create_icon_button(
        self,
        icon,
        size="medium",
        background_color="top_bar_button",
        icon_color="icon",
        **kwargs,
    ):

        button_size = self.theme.dimension(
            "button",
            "height",
        )


        button = MDIconButton(

            icon=icon,

            icon_size=self.theme.icon_size(
                size
            ),

            size_hint=(None, None),

            size=(
                button_size,
                button_size,
            ),

            theme_icon_color="Custom",

            **kwargs,
        )


        # ------------------------------------------------
        # Store application design tokens
        # ------------------------------------------------

        button.app_icon_color = (
            icon_color
        )

        button.app_background_color = (
            background_color
        )


        # ------------------------------------------------
        # Initial icon color
        # ------------------------------------------------

        icon_value = self.theme.get(
            icon_color
        )

        if icon_value is not None:

            button.icon_color = (
                icon_value
            )


        # ------------------------------------------------
        # Initial background color
        # ------------------------------------------------

        if background_color:

            background_value = self.theme.get(
                background_color
            )

            if background_value is not None:

                button.md_bg_color = (
                    background_value
                )


        return button


    # ====================================================
    # Standard button
    # ====================================================

    def create_button(
        self,
        text="",
        background_color="button",
        text_color="text_primary",
        **kwargs,
    ):

        button = MDRaisedButton(

            text=str(text),

            **kwargs,
        )


        # ------------------------------------------------
        # Store application design tokens
        # ------------------------------------------------

        button.app_background_color = (
            background_color
        )

        button.app_text_color = (
            text_color
        )


        # ------------------------------------------------
        # Initial background color
        # ------------------------------------------------

        if background_color:

            background = self.theme.get(
                background_color
            )

            if background is not None:

                button.md_bg_color = (
                    background
                )


        # ------------------------------------------------
        # Initial text color
        # ------------------------------------------------

        if text_color:

            color = self.theme.get(
                text_color
            )

            if color is not None:

                button.theme_text_color = (
                    "Custom"
                )

                button.text_color = (
                    color
                )


        return button


    # ====================================================
    # Apply button theme
    # ====================================================

    def apply_button_theme(
        self,
        button,
        background_color=None,
        text_color=None,
    ):

        # ------------------------------------------------
        # Background
        # ------------------------------------------------

        if background_color is not None:

            button.app_background_color = (
                background_color
            )

            background = self.theme.get(
                background_color
            )

            if background is not None:

                button.md_bg_color = (
                    background
                )


        # ------------------------------------------------
        # Text
        # ------------------------------------------------

        if text_color is not None:

            button.app_text_color = (
                text_color
            )

            color = self.theme.get(
                text_color
            )

            if color is not None:

                button.theme_text_color = (
                    "Custom"
                )

                button.text_color = (
                    color
                )


    # ====================================================
    # Card text layout
    # ====================================================

    def create_card_text_layout(
        self,
        **kwargs,
    ):

        defaults = {

            "orientation": "vertical",

            "spacing": self.theme.spacing(
                "xs"
            ),

            "size_hint_y": 1,
        }


        defaults.update(
            kwargs
        )


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
        **kwargs,
    ):

        defaults = {

            "text": text,

            "style": "subtitle",

            "color": color,

            "size_hint_y": 1,

            "valign": "bottom",
        }


        defaults.update(
            kwargs
        )


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
        **kwargs,
    ):

        defaults = {

            "text": text,

            "style": "secondary",

            "color": color,

            "size_hint_y": 1,

            "valign": "top",
        }


        defaults.update(
            kwargs
        )


        return self.create_label(
            **defaults
        )

    # ====================================================
    # Text field
    # ====================================================

    def create_input(
        self,
        hint_text="",
        text_color="text_primary",
        **kwargs,
    ):

        field = MDTextField(
            hint_text=str(hint_text),

            input_filter="int",

            **kwargs,
        )

        # ------------------------------------------------
        # Store application design token
        # ------------------------------------------------

        field.app_text_color = text_color

        # ------------------------------------------------
        # Initial text color
        # ------------------------------------------------

        color = self.theme.get(
            text_color
        )

        if color is not None:

            field.theme_text_color = "Custom"

            field.text_color = color

        return field