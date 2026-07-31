from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel

from kivy.metrics import dp


class BaseScreen(MDScreen):

    def add_top_bar(self, layout, title):

        bar = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(56),
            spacing=dp(10),
            padding=[dp(5), 0]
        )


        home_button = MDIconButton(
            icon="arrow-left",
            theme_icon_color="Custom",
            icon_color=(1, 1, 1, 1),
            md_bg_color=(0.2, 0.6, 0.2, 1)
        )

        home_button.bind(
            on_release=self.go_home
        )


        title_label = MDLabel(
            text=title,
            font_style="H5",
            valign="center"
        )


        bar.add_widget(home_button)

        bar.add_widget(title_label)


        layout.add_widget(bar)


    def go_home(self, instance):

        self.manager.current = "home"