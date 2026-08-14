
from kivymd.uix.boxlayout import MDBoxLayout

class SectionHeader(MDBoxLayout):

    """
    Section title + information button.

    This is the exact visual behavior of the original
    NewGameScreen.add_section_title().
    """

    def __init__(
        self,
        title,
        help_text,
        widget_factory,
        theme,
        on_help,
        **kwargs,
    ):

        super().__init__(
            **kwargs
        )

        self.orientation = "horizontal"

        self.adaptive_height = True

        self.size_hint_x = None

        self.spacing = theme.spacing(
            "xs"
        )


        # ------------------------------------------------
        # Title
        # ------------------------------------------------

        self.title_label = (
            widget_factory.create_label(
                text=title,
                style="subtitle",
                color="text_primary",
                size_hint_x=None,
                size_hint_y=None,
                adaptive_width=True,
                adaptive_height=True,
            )
        )


        # ------------------------------------------------
        # Information button
        # ------------------------------------------------

        self.info_button = (
            widget_factory.create_icon_button(
                icon="information-outline",
                size="medium",
                background_color=None,
                icon_color="icon",
            )
        )


        if on_help is not None:

            self.info_button.bind(
                on_release=lambda instance:
                    on_help(
                        str(title),
                        str(help_text),
                    )
            )


        # ------------------------------------------------
        # Assemble
        # ------------------------------------------------

        self.add_widget(
            self.title_label
        )

        self.add_widget(
            self.info_button
        )
