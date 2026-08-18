from .baseScreen import BaseScreen

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.progressbar import MDProgressBar

from widgets.trophy_card import TrophyCard


class TrophyScreen(BaseScreen):

    """
    Application trophy screen.

    Responsibilities:

        - Display trophy progress.
        - Display trophy cards.
        - Handle trophy-specific UI refresh.

    Shared theme, background, typography, dimensions,
    widget creation, and top bar behavior are provided
    by BaseScreen.
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # ====================================================
        # Main layout
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

        self.add_widget(
            self.layout
        )

        # ====================================================
        # Screen
        # ====================================================

        self.build_screen()

    # ====================================================
    # Build
    # ====================================================

    def build_screen(self):

        self.layout.clear_widgets()

        # ----------------------------------------------------
        # Top bar
        # ----------------------------------------------------

        self.add_top_bar(
            self.layout,
            "trophy_title",
        )

        # ----------------------------------------------------
        # Progress label
        # ----------------------------------------------------

        self.progress_label = self.create_label(
            style="body",
            color="text_secondary",

            halign="center",

            size_hint_y=None,
        )

        self.progress_label.bind(
            texture_size=lambda instance, value:
            setattr(
                instance,
                "height",
                value[1],
            )
        )

        self.layout.add_widget(
            self.progress_label
        )

        # ----------------------------------------------------
        # Progress bar
        # ----------------------------------------------------

        self.progress = MDProgressBar(
            value=0,
            max=100,

            size_hint_y=None,

            height=self.dimension(
                "progress",
                "height",
            ),
        )

        self.layout.add_widget(
            self.progress
        )

        # ----------------------------------------------------
        # Trophy scroll
        # ----------------------------------------------------

        scroll = MDScrollView()

        self.container = MDGridLayout(
            cols=3,

            spacing=self.spacing(
                "sm"
            ),

            padding=self.spacing(
                "sm"
            ),

            adaptive_height=True,
        )

        scroll.add_widget(
            self.container
        )

        self.layout.add_widget(
            scroll
        )

        # ----------------------------------------------------
        # Initial refresh
        # ----------------------------------------------------

        self.refresh_ui()

    # ====================================================
    # Lifecycle
    # ====================================================

    def on_pre_enter(self):

        super().on_pre_enter()

        self.refresh_ui()

    # ====================================================
    # UI refresh
    # ====================================================

    def refresh_ui(self):

        self.update_text()
        self.refresh_trophies()

    # ====================================================
    # Theme
    # ====================================================

    def refresh_screen_theme(self):

        if not hasattr(
            self,
            "progress",
        ):
            return

        progress_color = self.theme_manager.get(
            "progress"
        )

        if progress_color is not None:

            self.progress.color = (
                progress_color
            )

    # ====================================================
    # Translation
    # ====================================================

    def update_text(self):

        if not hasattr(
            self,
            "progress_label",
        ):
            return

        trophies = self.data.trophies

        total = len(
            trophies
        )

        unlocked = sum(
            1
            for trophy in trophies
            if trophy.unlocked
        )

        self.progress_label.text = (
            self.language_manager.get(
                "trophies_progress"
            ).format(
                unlocked=unlocked,
                total=total,
            )
        )

    # ====================================================
    # Trophies
    # ====================================================

    def refresh_trophies(self):

        if not hasattr(
            self,
            "container",
        ):
            return

        self.container.clear_widgets()

        trophies = self.data.trophies

        total = len(
            trophies
        )

        unlocked = sum(
            1
            for trophy in trophies
            if trophy.unlocked
        )

        # ----------------------------------------------------
        # Progress
        # ----------------------------------------------------

        if total > 0:

            self.progress.value = (
                unlocked / total * 100
            )

        else:

            self.progress.value = 0

        # ----------------------------------------------------
        # Trophy cards
        # ----------------------------------------------------

        for trophy in trophies:

            card = TrophyCard(
                trophy
            )

            self.container.add_widget(
                card
            )