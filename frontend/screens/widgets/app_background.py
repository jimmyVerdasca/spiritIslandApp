from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image


class AppBackground(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.background_image = Image(
            source="assets/home/island.png",
            size_hint=(1.12, 1.12),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.5,
            },
            fit_mode="cover",
        )

        self.add_widget(self.background_image)

        Clock.schedule_once(
            self.start_animation,
            0.1
        )

    def start_animation(self, *args):

        background_animation = (
            Animation(
                pos_hint={
                    "center_x": 0.48,
                    "center_y": 0.52,
                },
                duration=18,
            )
            +
            Animation(
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