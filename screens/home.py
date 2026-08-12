from .baseScreen import BaseScreen

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel


class HomeScreen(BaseScreen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # --------------------------------------------
        # Managers
        # --------------------------------------------

        app = MDApp.get_running_app()

        self.settings_manager = app.settings_manager
        self.language_manager = app.language_manager
        self.theme_manager = app.theme_manager


        # --------------------------------------------
        # Root
        # --------------------------------------------

        self.root_layout = FloatLayout()


        # --------------------------------------------
        # Background overlay
        # --------------------------------------------

        self.background_overlay = MDBoxLayout(
            size_hint=(1, 1),
            pos_hint={
                "x": 0,
                "y": 0,
            },
        )


        self.root_layout.add_widget(
            self.background_overlay
        )


        # --------------------------------------------
        # Main content
        # --------------------------------------------

        self.layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=[
                dp(24),
                dp(24),
                dp(24),
                dp(24),
            ],
        )


        # --------------------------------------------
        # Header
        # --------------------------------------------

        self.header = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(2),
        )


        self.header.bind(
            minimum_height=lambda instance, value:
            setattr(
                instance,
                "height",
                value
            )
        )


        self.title = MDLabel(
            halign="center",
            valign="middle",
            font_style="H4",
            size_hint_y=None,
        )


        self.title.bind(
            width=lambda instance, value:
            setattr(
                instance,
                "text_size",
                (value, None)
            )
        )


        self.title.bind(
            texture_size=lambda instance, value:
            setattr(
                instance,
                "height",
                value[1] + dp(10)
            )
        )


        self.description = MDLabel(
            font_style="Subtitle1",
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=dp(45),
        )


        self.description.bind(
            size=lambda instance, value:
            setattr(
                instance,
                "text_size",
                value
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


        # --------------------------------------------
        # Menu container
        # --------------------------------------------

        self.menu_container = MDBoxLayout(
            orientation="vertical",
            spacing=dp(8),
        )


        self.layout.add_widget(
            self.menu_container
        )


        # --------------------------------------------
        # Footer
        # --------------------------------------------

        self.footer = MDLabel(
            halign="center",
            size_hint_y=None,
            height=dp(35),
        )


        self.layout.add_widget(
            self.footer
        )


        # --------------------------------------------
        # Add content
        # --------------------------------------------

        self.root_layout.add_widget(
            self.layout
        )


        self.add_widget(
            self.root_layout
        )


        # --------------------------------------------
        # Menu cards
        # --------------------------------------------

        self.menu_cards = []


        # --------------------------------------------
        # Initial UI
        # --------------------------------------------

        self.refresh_ui()


    # ====================================================
    # Screen lifecycle
    # ====================================================

    def on_pre_enter(self):

        self.refresh_ui()


    # ====================================================
    # Refresh UI
    # ====================================================

    def refresh_ui(self):

        self.update_text()

        self.update_theme()

        self.build_menu()


    # ====================================================
    # Translations
    # ====================================================

    def update_text(self):

        self.title.text = (
            self.language_manager.get(
                "app_title"
            )
        )


        self.description.text = (
            self.language_manager.get(
                "home_subtitle"
            )
        )


        self.footer.text = (
            self.language_manager.get(
                "choose_adventure"
            )
        )


    # ====================================================
    # Theme
    # ====================================================

    def update_theme(self):

        self.background_overlay.md_bg_color = (
            self.theme_manager.get(
                "background_overlay"
            )
        )


        # --------------------------------------------
        # Title
        # --------------------------------------------

        self.title.theme_text_color = "Custom"

        self.title.text_color = (
            self.theme_manager.get(
                "text_primary"
            )
        )


        # --------------------------------------------
        # Description
        # --------------------------------------------

        self.description.theme_text_color = "Custom"

        self.description.text_color = (
            self.theme_manager.get(
                "text_secondary"
            )
        )


        # --------------------------------------------
        # Footer
        # --------------------------------------------

        self.footer.theme_text_color = "Custom"

        self.footer.text_color = (
            self.theme_manager.get(
                "text_muted"
            )
        )


    # ====================================================
    # Menu
    # ====================================================

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
                "trophies",
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


        # --------------------------------------------
        # Start animation
        # --------------------------------------------

        Clock.schedule_once(
            self.start_animations,
            0.05
        )


    # ====================================================
    # Build menu card
    # ====================================================

    def build_menu_card(
        self,
        title_key,
        description_key,
        screen,
        icon,
    ):

        card = MDCard(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(78),
            padding=dp(10),
            spacing=dp(10),
            radius=[18],
            elevation=3,
            opacity=0,
        )


        card.screen_name = screen


        # --------------------------------------------
        # Icon
        # --------------------------------------------

        icon_button = MDIconButton(
            icon=icon,
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            pos_hint={
                "center_y": 0.5,
            },
        )


        icon_button.bind(
            on_release=lambda instance, s=screen:
            self.navigate_to(s)
        )


        card.add_widget(
            icon_button
        )


        # --------------------------------------------
        # Text
        # --------------------------------------------

        text_layout = MDBoxLayout(
            orientation="vertical",
            spacing=0,
        )


        menu_title = MDLabel(
            text=self.language_manager.get(
                title_key
            ),
            font_style="H6",
            theme_text_color="Custom",
            size_hint_y=None,
            height=dp(32),
        )


        menu_description = MDLabel(
            text=self.language_manager.get(
                description_key
            ),
            theme_text_color="Custom",
            size_hint_y=None,
            height=dp(26),
        )


        text_layout.add_widget(
            menu_title
        )


        text_layout.add_widget(
            menu_description
        )


        card.add_widget(
            text_layout
        )


        # --------------------------------------------
        # Theme
        # --------------------------------------------

        self.apply_card_theme(
            card,
            icon_button,
            menu_title,
            menu_description,
        )


        # --------------------------------------------
        # Whole card clickable
        # --------------------------------------------

        card.bind(
            on_touch_up=self.card_pressed
        )


        return card


    # ====================================================
    # Card theme
    # ====================================================

    def apply_card_theme(
        self,
        card,
        icon_button,
        menu_title,
        menu_description,
    ):

        # --------------------------------------------
        # Get current theme
        # --------------------------------------------

        card_color = self.theme_manager.get(
            "card"
        )

        primary_color = self.theme_manager.get(
            "text_primary"
        )

        card_secondary_color = self.theme_manager.get(
            "card_text_secondary"
        )

        icon_color = self.theme_manager.get(
            "icon"
        )


        # --------------------------------------------
        # Card
        # --------------------------------------------

        card.md_bg_color = card_color


        # --------------------------------------------
        # Card title
        # --------------------------------------------

        menu_title.theme_text_color = "Custom"

        menu_title.text_color = primary_color


        # --------------------------------------------
        # Card description
        # --------------------------------------------

        menu_description.theme_text_color = "Custom"

        menu_description.text_color = card_secondary_color


        # --------------------------------------------
        # Icon
        # --------------------------------------------

        icon_button.theme_icon_color = "Custom"

        icon_button.icon_color = icon_color


    # ====================================================
    # Card interaction
    # ====================================================

    def card_pressed(self, card, touch):

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

    def start_animations(self, *args):

        for index, card in enumerate(
            self.menu_cards
        ):

            Clock.schedule_once(
                lambda dt, c=card:
                self.animate_card(c),
                0.08 * index,
            )


    def animate_card(self, card):

        Animation(
            opacity=1,
            duration=0.35,
            t="out_quad",
        ).start(
            card
        )


