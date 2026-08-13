from .baseScreen import BaseScreen

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout

from kivymd.uix.boxlayout import MDBoxLayout


class HomeScreen(BaseScreen):

    """
    Application home screen.
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.root_layout = FloatLayout()

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

        self.root_layout.add_widget(
            self.background_overlay
        )


        # ====================================================
        # Main content
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

        self.root_layout.add_widget(
            self.layout
        )


        # ====================================================
        # Header
        # ====================================================

        self.header = MDBoxLayout(
            orientation="vertical",

            size_hint_y=None,

            spacing=self.spacing(
                "xs"
            ),
        )

        self.header.bind(
            minimum_height=self.header.setter(
                "height"
            )
        )


        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

        self.title = self.create_label(
            style="display",
            color="text_primary",

            halign="center",
            valign="middle",

            size_hint_y=None,
        )

        self.title.bind(
            width=lambda instance, value:
            setattr(
                instance,
                "text_size",
                (value, None),
            )
        )

        self.title.bind(
            texture_size=lambda instance, value:
            setattr(
                instance,
                "height",
                value[1] + self.spacing(
                    "sm"
                ),
            )
        )


        # ----------------------------------------------------
        # Description
        # ----------------------------------------------------

        self.description = self.create_label(
            style="body",
            color="text_secondary",

            halign="center",
            valign="middle",

            size_hint_y=None,
        )

        self.description.bind(
            texture_size=lambda instance, value:
            setattr(
                instance,
                "height",
                value[1],
            )
        )

        self.description.bind(
            width=lambda instance, value:
            setattr(
                instance,
                "text_size",
                (value, None),
            )
        )


        self.header.add_widget(
            self.title
        )

        self.header.add_widget(
            self.description
        )

        self.layout.add_widget(
            self.header
        )


        # ====================================================
        # Menu
        # ====================================================

        self.menu_container = MDBoxLayout(
            orientation="vertical",

            spacing=self.spacing(
                "sm"
            ),
        )

        self.layout.add_widget(
            self.menu_container
        )


        # ====================================================
        # Footer
        # ====================================================

        self.footer = self.create_label(
            style="secondary",
            color="text_muted",

            halign="center",

            size_hint_y=None,

            height=self.dimension(
                "button",
                "height",
            ),
        )

        self.layout.add_widget(
            self.footer
        )

        self.add_widget(
            self.root_layout
        )

        self.menu_cards = []

        self.refresh_ui()



    def on_pre_enter(self):

        super().on_pre_enter()

        self.refresh_ui()


    def refresh_ui(self):

        self.update_text()
        self.build_menu()


    def update_text(self):

        self.title.text = str(
            self.language_manager.get(
                "app_title"
            )
        )

        self.description.text = str(
            self.language_manager.get(
                "home_subtitle"
            )
        )

        self.footer.text = str(
            self.language_manager.get(
                "choose_adventure"
            )
        )

    def build_menu(self):

        self.menu_container.clear_widgets()

        self.menu_cards = []


        menu = [

            (
                "new_game",
                "new_game_description",
                "new",
                "plus-circle-outline",
            ),

            (
                "current_games",
                "current_games_description",
                "current",
                "sword-cross",
            ),

            (
                "history",
                "history_description",
                "history",
                "history",
            ),

            (
                "trophy_title",
                "trophies_description",
                "trophies",
                "trophy-outline",
            ),

            (
                "settings",
                "settings_description",
                "settings",
                "cog-outline",
            ),
        ]


        for (
            title_key,
            description_key,
            screen,
            icon,
        ) in menu:

            card = self.build_menu_card(
                title_key,
                description_key,
                screen,
                icon,
            )

            self.menu_container.add_widget(
                card
            )

            self.menu_cards.append(
                card
            )


        Clock.schedule_once(
            self.start_animations,
            0.05,
        )

    def refresh_screen_theme(self):
    
        background = self.theme_manager.get(
            "background_overlay"
        )

        if background is not None:
            self.background_overlay.md_bg_color = background

    def build_menu_card(
        self,
        title_key,
        description_key,
        screen,
        icon,
    ):

        # ------------------------------------------------
        # Card
        # ------------------------------------------------

        card = self.create_card(
            opacity=0,
        )

        card.screen_name = screen


        # ------------------------------------------------
        # Icon
        # ------------------------------------------------

        icon_button = self.create_icon_button(
            icon=icon,
            background_color="card",
            icon_color="icon",
        )

        icon_button.pos_hint = {
            "center_y": 0.5,
        }

        icon_button.bind(
            on_release=lambda instance,
            s=screen:
            self.navigate_to(s)
        )


        # ------------------------------------------------
        # Text
        # ------------------------------------------------

        text_layout = (
            self.create_card_text_layout()
        )


        menu_title = self.create_card_title(
            text=str(
                self.language_manager.get(
                    title_key
                )
            )
        )


        menu_description = (
            self.create_card_description(
                text=str(
                    self.language_manager.get(
                        description_key
                    )
                )
            )
        )


        # ------------------------------------------------
        # Build text layout
        # ------------------------------------------------

        text_layout.add_widget(
            menu_title
        )

        text_layout.add_widget(
            menu_description
        )


        # ------------------------------------------------
        # Build card
        # ------------------------------------------------

        card.add_widget(
            icon_button
        )

        card.add_widget(
            text_layout
        )


        # ------------------------------------------------
        # Interaction
        # ------------------------------------------------

        card.bind(
            on_touch_up=self.card_pressed
        )


        return card


    # ====================================================
    # Card interaction
    # ====================================================

    def card_pressed(
        self,
        card,
        touch,
    ):

        if not card.collide_point(
            *touch.pos
        ):
            return False


        self.navigate_to(
            card.screen_name
        )

        return True


    # ====================================================
    # Animations
    # ====================================================

    def start_animations(
        self,
        *args,
    ):

        for index, card in enumerate(
            self.menu_cards
        ):

            Clock.schedule_once(
                lambda dt, c=card:
                self.animate_card(c),

                0.08 * index,
            )


    def animate_card(
        self,
        card,
    ):

        Animation(
            opacity=1,

            duration=0.35,

            t="out_quad",
        ).start(card)
