
from kivymd.uix.boxlayout import MDBoxLayout

class SelectionRow(MDBoxLayout):

    """
    Generic horizontal selection row.

    Used by NewGameScreen for:

        - adversaries
        - scenarios

    The actual selection logic remains in NewGameScreen.
    """

    def __init__(
        self,
        widget_factory,
        theme,
        main_text="",
        main_size_hint_x=1,
        secondary_text=None,
        secondary_size_hint_x=0.25,
        on_main=None,
        on_secondary=None,
        on_remove=None,
        **kwargs,
    ):

        super().__init__(
            **kwargs
        )

        self.widget_factory = widget_factory
        self.theme = theme

        self.orientation = "horizontal"

        self.spacing = theme.spacing(
            "sm"
        )

        self.adaptive_height = True


        # ------------------------------------------------
        # Main button
        # ------------------------------------------------

        self.main_button = (
            widget_factory.create_button(
                text=main_text,
                size_hint_x=main_size_hint_x,
            )
        )


        self.add_widget(
            self.main_button
        )


        # ------------------------------------------------
        # Secondary button
        # ------------------------------------------------

        self.secondary_button = None

        if secondary_text is not None:

            self.secondary_button = (
                widget_factory.create_button(
                    text=secondary_text,
                    size_hint_x=secondary_size_hint_x,
                )
            )

            self.add_widget(
                self.secondary_button
            )


        # ------------------------------------------------
        # Remove button
        # ------------------------------------------------

        self.remove_button = (
            widget_factory.create_icon_button(
                icon="close",
                size="medium",
                background_color=None,
                icon_color="icon",
            )
        )


        self.add_widget(
            self.remove_button
        )


        # ------------------------------------------------
        # Bind callbacks
        # ------------------------------------------------

        if on_main is not None:

            self.main_button.bind(
                on_release=on_main
            )


        if (
            self.secondary_button is not None
            and on_secondary is not None
        ):

            self.secondary_button.bind(
                on_release=on_secondary
            )


        if on_remove is not None:

            self.remove_button.bind(
                on_release=on_remove
            )