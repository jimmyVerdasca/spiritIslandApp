from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from kivy.uix.image import Image
from kivy.metrics import dp


class TrophyCard(MDCard):

    TROPHY_IMAGE_PATH = "assets/trophies/"

    def __init__(self, trophy, **kwargs):

        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.padding = dp(10)
        self.spacing = dp(5)

        self.size_hint_y = None
        self.height = dp(200)


        image = Image(
            source=(
                self.TROPHY_IMAGE_PATH + trophy.unlocked_image
                if trophy.unlocked
                else self.TROPHY_IMAGE_PATH + trophy.locked_image
            ),
            allow_stretch=True,
            keep_ratio=True,
        )

        self.add_widget(image)


        self.add_widget(
            MDLabel(
                text=trophy.name,
                halign="center",
                bold=True,
                adaptive_height=True,
            )
        )


        self.add_widget(
            MDLabel(
                text=trophy.description,
                halign="center",
                adaptive_height=True,
            )
        )


        if trophy.unlocked:

            self.md_bg_color = (
                0.8,
                1,
                0.8,
                1
            )

        else:

            self.md_bg_color = (
                0.7,
                0.7,
                0.7,
                1
            )