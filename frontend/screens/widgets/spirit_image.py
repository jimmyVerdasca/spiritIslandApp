from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from theme import get_theme
from theme.translations import t


SPIRIT_IMAGE_PATH = "assets/spirits/"


class SpiritImage(MDCard):

    spirit = ObjectProperty(None, allownone=True)

    def __init__(self, spirit=None, **kwargs):

        super().__init__(**kwargs)

        self.spirit = spirit
        self._pressed = False

        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = dp(210)

        self.radius = [dp(18)]
        self.elevation = 3
        self.padding = 0

        theme = get_theme()

        artwork = FloatLayout()

        # ------------------------------------------------
        # Artwork
        # ------------------------------------------------

        self.image = Image(
            source="",
            size_hint=(1, 1),
            pos_hint={
                "x": 0,
                "y": 0,
            },
            allow_stretch=True,
            keep_ratio=True,
        )

        artwork.add_widget(self.image)

        # ------------------------------------------------
        # Empty state
        # ------------------------------------------------

        self.empty_overlay = MDBoxLayout(
            orientation="vertical",
            size_hint=(None, None),
            size=(dp(180), dp(90)),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.55,
            },
        )

        self.empty_icon = MDLabel(
            text="✦",
            halign="center",
            font_style="H4",
            theme_text_color="Custom",
            text_color=theme["text_secondary"],
        )

        self.empty_label = MDLabel(
            text=t("choose_spirit"),
            halign="center",
            theme_text_color="Custom",
            text_color=theme["text_secondary"],
            bold=True,
        )

        self.empty_overlay.add_widget(
            self.empty_icon
        )

        self.empty_overlay.add_widget(
            self.empty_label
        )

        artwork.add_widget(
            self.empty_overlay
        )

        # ------------------------------------------------
        # Name
        # ------------------------------------------------

        self.name_background = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            height=dp(48),
            pos_hint={
                "x": 0,
                "y": 0,
            },
        )

        self.name_background.md_bg_color = (
            theme["card_overlay"]
        )

        self.name_label = MDLabel(
            text=t("any_spirit"),
            halign="center",
            valign="middle",
            theme_text_color="Custom",
            text_color=theme["text_primary"],
            bold=True,
        )

        self.name_background.add_widget(
            self.name_label
        )

        artwork.add_widget(
            self.name_background
        )

        self.add_widget(
            artwork
        )

        self.register_event_type(
            "on_release"
        )

        self.set_spirit(spirit)

    # ----------------------------------------------------
    # Spirit
    # ----------------------------------------------------

    def set_spirit(self, spirit):

        self.spirit = spirit

        theme = get_theme()

        if spirit is None:

            self.image.source = ""

            self.name_label.text = t(
                "any_spirit"
            )

            self.empty_label.text = t(
                "choose_spirit"
            )

            self.empty_overlay.opacity = 1

            self.md_bg_color = (
                theme["card"]
            )

        else:

            # The key is used for the asset filename
            self.image.source = (
                f"{SPIRIT_IMAGE_PATH}"
                f"{spirit.key}.png"
            )

            # The key is translated for display
            self.name_label.text = t(
                spirit.key,
                "spirits"
            )

            self.empty_overlay.opacity = 0

            self.md_bg_color = (
                theme["card"]
            )

    # ----------------------------------------------------
    # Touch
    # ----------------------------------------------------

    def on_touch_down(self, touch):

        if not self.collide_point(
            *touch.pos
        ):
            return super().on_touch_down(
                touch
            )

        self._pressed = True

        theme = get_theme()

        self.md_bg_color = (
            theme["card_pressed"]
        )

        return True

    def on_touch_up(self, touch):

        if not self._pressed:
            return super().on_touch_up(
                touch
            )

        self._pressed = False

        theme = get_theme()

        self.md_bg_color = (
            theme["card"]
        )

        self.dispatch(
            "on_release"
        )

        return True

    def on_release(self):
        pass