from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel


class HomeScreen(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # ------------------------------------------------
        # Root
        # ------------------------------------------------

        root = FloatLayout()

        # ------------------------------------------------
        # Background
        # ------------------------------------------------

        self.background_image = Image(
            source="assets/home/island.png",
            size_hint=(1.12, 1.12),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.5,
            },
            fit_mode="cover",
        )

        root.add_widget(
            self.background_image
        )

        # ------------------------------------------------
        # Dark overlay
        # ------------------------------------------------

        background_overlay = MDBoxLayout(
            size_hint=(1, 1),
            pos_hint={
                "x": 0,
                "y": 0,
            },
        )

        background_overlay.md_bg_color = (
            0,
            0,
            0,
            0.50,
        )

        root.add_widget(
            background_overlay
        )

        # ------------------------------------------------
        # Main content
        # ------------------------------------------------

        layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(16),
            padding=dp(24),
        )

        # ------------------------------------------------
        # Header
        # ------------------------------------------------

        header = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(2),
        )

        header.bind(
            minimum_height=lambda instance, value:
            setattr(instance, "height", value)
        )

        title = MDLabel(
            text="Spirit Island Companion",
            halign="center",
            valign="middle",
            font_style="H4",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
        )

        title.bind(
            width=lambda instance, value:
            setattr(instance, "text_size", (value, None))
        )

        title.bind(
            texture_size=lambda instance, value:
            setattr(instance, "height", value[1] + dp(10))
        )

        description = MDLabel(
            text=(
                "Plan your game. Track your progress.\n"
                "Face the island's next challenge."
            ),
            font_style="Subtitle1",
            halign="center",
            valign="middle",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.80),
            size_hint_y=None,
            height=dp(45),
        )

        description.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", value)
        )

        header.add_widget(title)
        header.add_widget(description)

        layout.add_widget(header)

        # ------------------------------------------------
        # Menu
        # ------------------------------------------------

        menu = [
            (
                "New Game",
                "Create a new Spirit Island game",
                "new",
                "plus-circle-outline",
            ),
            (
                "Current Games",
                "Browse and manage your current games",
                "current",
                "sword-cross",
            ),
            (
                "History",
                "Review your previous games",
                "history",
                "history",
            ),
            (
                "Trophies",
                "View your achievements",
                "trophies",
                "trophy-outline",
            ),
        ]

        self.menu_cards = []

        for text, description_text, screen, icon in menu:

            # --------------------------------------------
            # Card
            # --------------------------------------------

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

            card.md_bg_color = (
                0.05,
                0.05,
                0.05,
                0.78,
            )

            # Store destination on the card
            card.screen_name = screen

            # --------------------------------------------
            # Icon
            # --------------------------------------------

            icon_button = MDIconButton(
                icon=icon,
                theme_icon_color="Custom",
                icon_color=(1, 1, 1, 1),
                size_hint=(None, None),
                size=(dp(50), dp(50)),
                pos_hint={
                    "center_y": 0.5,
                },
            )

            # Clicking the icon also navigates.
            icon_button.bind(
                on_release=lambda instance, s=screen:
                self.change_screen(s)
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
                text=text,
                font_style="H6",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                size_hint_y=None,
                height=dp(32),
            )

            menu_description = MDLabel(
                text=description_text,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 0.65),
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
            # Whole card is clickable
            # --------------------------------------------

            card.bind(
                on_touch_up=self.card_pressed
            )

            # --------------------------------------------
            # Add card
            # --------------------------------------------

            layout.add_widget(
                card
            )

            self.menu_cards.append(
                card
            )

        # ------------------------------------------------
        # Footer
        # ------------------------------------------------

        footer = MDLabel(
            text="Choose your next adventure",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.55),
            size_hint_y=None,
            height=dp(35),
        )

        layout.add_widget(
            footer
        )

        # ------------------------------------------------
        # Add content
        # ------------------------------------------------

        root.add_widget(
            layout
        )

        self.add_widget(
            root
        )

        # ------------------------------------------------
        # Start animations
        # ------------------------------------------------

        Clock.schedule_once(
            self.start_animations,
            0.15
        )

    # ====================================================
    # Card interaction
    # ====================================================

    def card_pressed(self, card, touch):

        if not card.collide_point(
            *touch.pos
        ):
            return False

        self.change_screen(
            card.screen_name
        )

        return True

    # ====================================================
    # Animations
    # ====================================================

    def start_animations(self, *args):

        # ------------------------------------------------
        # Background movement
        # ------------------------------------------------

        background_animation = (
            Animation(
                pos_hint={
                    "center_x": 0.48,
                    "center_y": 0.52,
                },
                duration=18,
            )
            + Animation(
                pos_hint={
                    "center_x": 0.52,
                    "center_y": 0.48,
                },
                duration=18,
            )
        )

        background_animation.repeat = True

        background_animation.start(
            self.background_image
        )

        # ------------------------------------------------
        # Staggered card appearance
        # ------------------------------------------------

        for index, card in enumerate(
            self.menu_cards
        ):

            Clock.schedule_once(
                lambda dt, c=card:
                self.animate_card(c),
                0.12 * index,
            )

    def animate_card(self, card):

        Animation(
            opacity=1,
            duration=0.35,
            t="out_quad",
        ).start(
            card
        )

    # ====================================================
    # Navigation
    # ====================================================

    def change_screen(self, screen):

        print(
            "Switching to",
            screen
        )

        self.manager.current = screen