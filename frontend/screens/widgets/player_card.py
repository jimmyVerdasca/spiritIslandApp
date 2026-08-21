from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard

from frontend.managers.assets_manager import AssetManager


class PlayerCard(MDCard):

    def __init__(
        self,
        player_number,
        widget_factory,
        theme,
        language_manager,
        on_spirit=None,
        on_board=None,
        **kwargs,
    ):

        super().__init__(
            **kwargs
        )

        # =================================================
        # State
        # =================================================

        self.player_number = player_number
        self.widget_factory = widget_factory
        self.theme = theme
        self.language_manager = language_manager

        self.on_spirit = on_spirit
        self.on_board = on_board

        self.spirit = None
        self.board = None

        self.spirit_image = None
        self.board_image = None

        self.spirit_name_label = None
        self.board_name_label = None

        self.spirit_button = None
        self.board_button = None

        self.player_title = None

        # =================================================
        # Build
        # =================================================

        self.build()


    # ====================================================
    # Translation
    # ====================================================

    def t(
        self,
        key,
        *categories,
    ):

        value = self.language_manager.get(
            key,
            *categories,
        )

        if isinstance(value, str):
            return value

        return str(value)


    # ====================================================
    # Build
    # ====================================================

    def build(self):

        # =================================================
        # Card
        # =================================================

        self.orientation = "vertical"

        # IMPORTANT:
        # The parent players_container uses adaptive_height.
        # Therefore this card must provide its own explicit
        # height and must NOT use adaptive_height.
        self.size_hint_y = None
        self.adaptive_height = False

        self.padding = 0

        self.elevation = 2

        # -------------------------------------------------
        # Original card/image aspect ratio
        #
        # Original image:
        #     198 x 128
        #
        # Therefore:
        #     height = width / (198 / 128)
        # -------------------------------------------------

        image_ratio = 198 / 128

        def update_card_height(
            card,
            width,
            ratio=image_ratio,
        ):

            if width > 0:
                card.height = width / ratio


        self.bind(
            width=update_card_height
        )


        # =================================================
        # Background
        # =================================================

        background = FloatLayout(
            size_hint=(1, 1),
        )


        # =================================================
        # Spirit image
        # =================================================

        self.spirit_image = Image(
            source=AssetManager.path("spirits", "Any.png",),
            size_hint=(1, 1),
            pos_hint={
                "x": 0,
                "y": 0,
            },
            fit_mode="cover",
        )


        background.add_widget(
            self.spirit_image
        )


        # =================================================
        # Board container
        # =================================================

        board_container = FloatLayout(

            size_hint=(
                0.40,
                0.40,
            ),

            pos_hint={
                "right": 0.98,
                "top": 0.98,
            },
        )


        # =================================================
        # Board image
        # =================================================

        self.board_image = Image(
            source=AssetManager.path("boards", "Any.png",),
            size_hint=(1, 1),
            pos_hint={
                "x": 0,
                "y": -0.5,
            },
            fit_mode="contain",
        )


        board_container.add_widget(
            self.board_image
        )


        # =================================================
        # Board name overlay
        # =================================================

        board_title_overlay = MDBoxLayout(

            orientation="vertical",

            size_hint=(
                1,
                0.35,
            ),

            pos_hint={
                "x": 0,
                "center_y": 0,
            },
        )


        self.board_name_label = (
            self.widget_factory.create_label(

                text=self.t("any"),

                style="secondary",

                # Text is always displayed over the
                # dark player-card image.
                color="player_card_text",

                halign="center",

                valign="middle",

                size_hint_y=1,

                font_style="H6",
            )
        )


        self.board_name_label.bind(

            size=lambda instance, value:
                setattr(
                    instance,
                    "text_size",
                    value,
                )
        )


        board_title_overlay.add_widget(
            self.board_name_label
        )


        board_container.add_widget(
            board_title_overlay
        )


        background.add_widget(
            board_container
        )


        # =================================================
        # Main overlay
        # =================================================

        overlay = MDBoxLayout(

            orientation="vertical",

            size_hint=(1, 1),

            pos_hint={
                "x": 0,
                "y": 0,
            },

            padding=self.theme.spacing(
                "sm"
            ),

            spacing=self.theme.spacing(
                "xs"
            ),
        )


        # =================================================
        # Player title
        # =================================================

        self.player_title = (
            self.widget_factory.create_label(

                text=(
                    f"{self.t('player')} "
                    f"{self.player_number}"
                ),

                style="subtitle",

                # Always white because it is over the
                # player-card image.
                color="player_card_text",

                size_hint_y=None,

                height=dp(30),

                font_style="H5",
            )
        )


        overlay.add_widget(
            self.player_title
        )


        # =================================================
        # Spirit name
        # =================================================

        self.spirit_name_label = (
            self.widget_factory.create_label(

                text="",

                style="subtitle",

                # Always white because it is over the
                # player-card image.
                color="player_card_text",

                size_hint_y=None,

                height=dp(30),

                halign="left",

                valign="middle",
            )
        )


        self.spirit_name_label.bind(

            width=lambda instance, value:
                setattr(
                    instance,
                    "text_size",
                    (
                        value,
                        None,
                    ),
                )
        )


        overlay.add_widget(
            self.spirit_name_label
        )


        # =================================================
        # Spacer
        # =================================================

        spacer = MDBoxLayout(
            size_hint_y=1,
        )


        overlay.add_widget(
            spacer
        )


        # =================================================
        # Buttons
        # =================================================

        button_row = MDBoxLayout(

            orientation="horizontal",

            size_hint_x=1,

            size_hint_y=None,

            height=self.theme.dimension(
                "button",
                "height",
            ),

            spacing=self.theme.spacing(
                "xs"
            ),
        )


        # -------------------------------------------------
        # Spirit button
        # -------------------------------------------------

        self.spirit_button = (
            self.widget_factory.create_button(

                text=self.t(
                    "choose_spirit"
                ),

                size_hint_x=0.55,
            )
        )


        # -------------------------------------------------
        # Board button
        # -------------------------------------------------

        self.board_button = (
            self.widget_factory.create_button(

                text=self.t(
                    "choose_board"
                ),

                size_hint_x=0.45,
            )
        )


        # =================================================
        # Callbacks
        # =================================================

        if self.on_spirit is not None:

            self.spirit_button.bind(
                on_release=self.on_spirit
            )


        if self.on_board is not None:

            self.board_button.bind(
                on_release=self.on_board
            )


        # =================================================
        # Assemble buttons
        # =================================================

        button_row.add_widget(
            self.spirit_button
        )

        button_row.add_widget(
            self.board_button
        )


        overlay.add_widget(
            button_row
        )


        # =================================================
        # Assemble overlay
        # =================================================

        background.add_widget(
            overlay
        )


        # =================================================
        # Assemble card
        # =================================================

        self.add_widget(
            background
        )


    # ====================================================
    # Spirit
    # ====================================================

    def set_spirit(
        self,
        spirit,
    ):

        self.spirit = spirit

        if spirit is None:

            self.spirit_name_label.text = ""

            self.spirit_image.source = AssetManager.path("spirits", "Any.png")

        else:

            self.spirit_name_label.text = (
                self.spirit_name(
                    spirit
                )
            )

            self.spirit_image.source = AssetManager.path("spirits", f"{spirit.key}.png")


        # Make sure Kivy notices the image change.
        self.spirit_image.reload()


    # ====================================================
    # Board
    # ====================================================

    def set_board(
        self,
        board,
    ):

        self.board = board

        if board is None:

            self.board_name_label.text = (
                self.t("any")
            )

            self.board_image.source = AssetManager.path("boards", "Any.png")

        else:

            self.board_name_label.text = (
                self.board_name(
                    board
                )
            )

            self.board_image.source = AssetManager.path("boards", f"{board.key}.png")


        # Make sure Kivy notices the image change.
        self.board_image.reload()


    # ====================================================
    # Spirit name
    # ====================================================

    def spirit_name(
        self,
        spirit,
    ):

        key = self.object_key(
            spirit
        )

        return self.t(
            key,
            "spirits",
        )


    # ====================================================
    # Board name
    # ====================================================

    def board_name(
        self,
        board,
    ):

        key = self.object_key(
            board
        )

        return self.t(
            key,
            "boards",
        )


    # ====================================================
    # Object key helper
    # ====================================================

    @staticmethod
    def object_key(
        value,
    ):

        if hasattr(
            value,
            "key",
        ):

            return value.key


        if hasattr(
            value,
            "slug",
        ):

            return value.slug


        if hasattr(
            value,
            "name",
        ):

            return (
                str(
                    value.name
                )
                .strip()
                .lower()
                .replace(
                    "'",
                    "",
                )
                .replace(
                    "-",
                    "_",
                )
                .replace(
                    " ",
                    "_",
                )
            )


        return str(value)