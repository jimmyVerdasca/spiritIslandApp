from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel

from kivy.metrics import dp
from kivy.uix.widget import Widget


class BaseScreen(MDScreen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.previous_screen = "home"


    def add_top_bar(self, layout, title):
    
        bar = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(56),
            spacing=dp(10),
            padding=[dp(5), 0],
        )

        back_button = MDIconButton(
            icon="arrow-left",
            theme_icon_color="Custom",
            icon_color=(1, 1, 1, 1),
            md_bg_color=(0.2, 0.6, 0.2, 1),
        )

        back_button.bind(on_release=self.go_back)

        self.top_bar_title = MDLabel(
            text=title,
            font_style="H5",
            valign="center",
        )

        settings_button = MDIconButton(
            icon="cog-outline",
            icon_size=dp(28),
            theme_icon_color="Custom",
            icon_color=(1, 1, 1, 1),
        )

        settings_button.bind(
            on_release=lambda instance: self.navigate_to("settings")
        )

        # Left side
        bar.add_widget(back_button)
        bar.add_widget(self.top_bar_title)

        # Empty space pushes settings button to the right
        spacer = Widget()
        bar.add_widget(spacer)

        # Right side
        bar.add_widget(settings_button)

        layout.add_widget(bar)



    def go_back(self, instance):

        self.manager.current = self.previous_screen



    def navigate_to(self, screen_name, previous=None, **kwargs):

        if self.manager.current == screen_name:
            return

        screen = self.manager.get_screen(screen_name)


        # Define where the back button returns
        if previous:
            screen.previous_screen = previous
        else:
            screen.previous_screen = self.name


        # Pass data to destination screen
        for key, value in kwargs.items():
            setattr(screen, key, value)


        self.manager.current = screen_name