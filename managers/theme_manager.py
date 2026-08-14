# ============================================================
# managers/theme_manager.py
# ============================================================

import copy
import importlib

from data.themes import THEMES


class ThemeManager:
    """
    Central manager for the application's design system.

    Handles:

        - Theme file selection
        - Light / dark themes
        - Color palette resolution
        - Shared dimensions
        - Typography
        - Component design tokens
        - Theme change listeners

    Theme files must expose:

        THEMES = {
            "palette": {...},
            "dark": {...},
            "light": {...},
            "dimensions": {...},
            "typography": {...},
        }
    """

    DEFAULT_THEME = "dark"
    DEFAULT_THEME_FILE = "themes"

    THEME_MODULES = {
        "themes": "data.themes",
        "sunset_ocean": "data.theme_test_sunset_ocean",
        "sunset_coral": "data.theme_test_sunset_coral",
        "deep_teal": "data.theme_test_deep_teal",
        "tropical_earth": "data.theme_test_tropical_earth",
        "forest_island": "data.theme_test_forest_island",
    }

    NON_THEME_SECTIONS = {
        "palette",
        "dimensions",
        "typography",
    }

    REQUIRED_SECTIONS = {
        "palette",
        "dimensions",
        "typography",
    }

    # Cached copies are important because data.themes.THEMES
    # is intentionally shared with the rest of the application.
    #
    # Without cached copies, switching:
    #
    #     themes -> sunset_ocean -> themes
    #
    # would not restore the original themes dictionary because
    # the original dictionary was already mutated.
    _THEME_CACHE = {}

    def __init__(
        self,
        theme=None,
        theme_file=None,
    ):

        self._theme_listeners = []

        # Must exist BEFORE load_theme_file().
        self.current_theme = None
        self.current_theme_file = self.DEFAULT_THEME_FILE

        # ----------------------------------------------------
        # Resolve theme file
        # ----------------------------------------------------

        if theme_file in self.available_theme_files():

            selected_theme_file = theme_file

        else:

            selected_theme_file = self.DEFAULT_THEME_FILE

        # ----------------------------------------------------
        # Load theme file
        # ----------------------------------------------------

        self.load_theme_file(
            selected_theme_file,
            notify=False,
        )

        # ----------------------------------------------------
        # Select light / dark theme
        # ----------------------------------------------------

        available = self.available_themes()

        if theme in available:

            self.current_theme = theme

        elif self.DEFAULT_THEME in available:

            self.current_theme = self.DEFAULT_THEME

        elif available:

            self.current_theme = available[0]

        else:

            raise ValueError(
                f"Theme file '{selected_theme_file}' "
                f"contains no usable themes."
            )

    # ========================================================
    # Theme files
    # ========================================================

    @classmethod
    def available_theme_files(cls):
        """
        Return available theme-file identifiers.
        """

        return list(
            cls.THEME_MODULES.keys()
        )

    @classmethod
    def get_theme_file_module(
        cls,
        theme_file,
    ):
        """
        Return the Python module path for a theme file.
        """

        return cls.THEME_MODULES.get(
            theme_file
        )

    @classmethod
    def _load_module_themes(
        cls,
        theme_file,
    ):
        """
        Import a theme module and return a cached deep copy
        of its original THEMES dictionary.

        Caching prevents the shared data.themes.THEMES
        dictionary from permanently replacing the original
        theme data.
        """

        if theme_file in cls._THEME_CACHE:

            return copy.deepcopy(
                cls._THEME_CACHE[
                    theme_file
                ]
            )

        module_name = cls.THEME_MODULES.get(
            theme_file
        )

        if module_name is None:

            raise ValueError(
                f"Unknown theme file: {theme_file}"
            )

        module = importlib.import_module(
            module_name
        )

        new_themes = getattr(
            module,
            "THEMES",
            None,
        )

        if not isinstance(
            new_themes,
            dict,
        ):

            raise ValueError(
                f"Theme module '{module_name}' "
                f"does not contain a valid THEMES dictionary."
            )

        cached_themes = copy.deepcopy(
            new_themes
        )

        cls._validate_themes(
            theme_file,
            cached_themes,
        )

        cls._THEME_CACHE[
            theme_file
        ] = cached_themes

        return copy.deepcopy(
            cached_themes
        )

    @classmethod
    def _validate_themes(
        cls,
        theme_file,
        themes,
    ):
        """
        Validate the basic structure of a theme file.
        """

        missing_sections = (
            cls.REQUIRED_SECTIONS
            - set(themes.keys())
        )

        if missing_sections:

            raise ValueError(
                f"Theme file '{theme_file}' is missing "
                f"required sections: "
                f"{sorted(missing_sections)}"
            )

        available_themes = [
            key
            for key, value in themes.items()
            if (
                isinstance(value, dict)
                and key not in cls.NON_THEME_SECTIONS
            )
        ]

        if not available_themes:

            raise ValueError(
                f"Theme file '{theme_file}' "
                f"contains no color themes."
            )

    def load_theme_file(
        self,
        theme_file,
        notify=True,
    ):
        """
        Load a complete THEMES dictionary.

        The shared data.themes.THEMES dictionary is mutated
        in place so existing imports continue to work.
        """

        if theme_file not in self.available_theme_files():

            raise ValueError(
                f"Unknown theme file: {theme_file}. "
                f"Available theme files: "
                f"{self.available_theme_files()}"
            )

        new_themes = self._load_module_themes(
            theme_file
        )

        available_themes = [
            key
            for key, value in new_themes.items()
            if (
                isinstance(value, dict)
                and key not in self.NON_THEME_SECTIONS
            )
        ]

        # ----------------------------------------------------
        # Remember current theme before replacing data.
        # ----------------------------------------------------

        previous_theme = self.current_theme

        # ----------------------------------------------------
        # Replace shared dictionary IN PLACE.
        # ----------------------------------------------------

        THEMES.clear()

        THEMES.update(
            new_themes
        )

        self.current_theme_file = (
            theme_file
        )

        # ----------------------------------------------------
        # Keep current light/dark theme where possible.
        # ----------------------------------------------------

        if previous_theme in available_themes:

            self.current_theme = previous_theme

        elif self.DEFAULT_THEME in available_themes:

            self.current_theme = (
                self.DEFAULT_THEME
            )

        else:

            self.current_theme = (
                available_themes[0]
            )

        # ----------------------------------------------------
        # Notify listeners.
        # ----------------------------------------------------

        if notify:

            self._notify_theme_change()

    def get_theme_file(self):
        """
        Return the currently selected theme file.
        """

        return self.current_theme_file

    # ========================================================
    # Themes
    # ========================================================

    def available_themes(self):
        """
        Return all light/dark themes in the currently loaded
        theme file.
        """

        return [
            key
            for key, value in THEMES.items()
            if (
                isinstance(value, dict)
                and key not in self.NON_THEME_SECTIONS
            )
        ]

    def set_theme(
        self,
        theme,
    ):
        """
        Change the active light/dark theme.
        """

        if theme not in self.available_themes():

            raise ValueError(
                f"Unknown theme: {theme}. "
                f"Available themes: "
                f"{self.available_themes()}"
            )

        if theme == self.current_theme:

            return

        self.current_theme = theme

        self._notify_theme_change()

    def get_theme(self):
        """
        Return the current light/dark theme.
        """

        return self.current_theme

    # ========================================================
    # Palette
    # ========================================================

    def _resolve_palette_reference(
        self,
        value,
    ):
        """
        Resolve values such as:

            palette.green.500
            palette.blue.700
        """

        if not isinstance(
            value,
            str,
        ):

            return value

        if not value.startswith(
            "palette."
        ):

            return value

        path = value.split(".")

        if len(path) < 3:

            raise ValueError(
                f"Invalid palette reference: {value}"
            )

        current = THEMES.get(
            "palette",
            {}
        )

        for part in path[1:]:

            if (
                not isinstance(
                    current,
                    dict,
                )
                or part not in current
            ):

                raise KeyError(
                    f"Unknown palette reference: "
                    f"{value}"
                )

            current = current[part]

        return current

    def get_palette(
        self,
        family=None,
        shade=None,
        default=None,
    ):
        """
        Get a palette family or shade.
        """

        palette = THEMES.get(
            "palette",
            {}
        )

        if family is None:

            return palette

        family_data = palette.get(
            family
        )

        if family_data is None:

            return default

        if shade is None:

            return family_data

        if not isinstance(
            family_data,
            dict,
        ):

            return default

        return family_data.get(
            shade,
            default,
        )

    # ========================================================
    # Colors
    # ========================================================

    def get(
        self,
        key,
        default=None,
    ):
        """
        Get a color/design token from the current theme.
        """

        theme = THEMES.get(
            self.current_theme,
            {}
        )

        if not isinstance(
            theme,
            dict,
        ):

            return default

        if key not in theme:

            return default

        value = theme[key]

        return self._resolve_palette_reference(
            value
        )

    # ========================================================
    # Dimensions
    # ========================================================

    def get_dimensions(
        self,
        section=None,
        key=None,
        default=None,
    ):
        """
        Get dimensions or component tokens.
        """

        dimensions = THEMES.get(
            "dimensions",
            {}
        )

        if section is None:

            return dimensions

        section_data = dimensions.get(
            section
        )

        if section_data is None:

            return default

        if key is None:

            return section_data

        if not isinstance(
            section_data,
            dict,
        ):

            return default

        return section_data.get(
            key,
            default,
        )

    # ========================================================
    # Typography
    # ========================================================

    def get_typography(
        self,
        style=None,
        key=None,
        default=None,
    ):
        """
        Get typography tokens.
        """

        typography = THEMES.get(
            "typography",
            {}
        )

        if style is None:

            return typography

        style_data = typography.get(
            style
        )

        if style_data is None:

            return default

        if key is None:

            return style_data

        if not isinstance(
            style_data,
            dict,
        ):

            return default

        return style_data.get(
            key,
            default,
        )

    # ========================================================
    # Component tokens
    # ========================================================

    def get_component(
        self,
        component,
        key=None,
        default=None,
    ):
        return self.get_dimensions(
            component,
            key,
            default,
        )

    # ========================================================
    # Spacing
    # ========================================================

    def spacing(
        self,
        size,
        default=None,
    ):
        return self.get_dimensions(
            "spacing",
            size,
            default,
        )

    # ========================================================
    # Icon sizes
    # ========================================================

    def icon_size(
        self,
        size,
        default=None,
    ):
        return self.get_dimensions(
            "icon",
            size,
            default,
        )

    # ========================================================
    # Typography helpers
    # ========================================================

    def font_size(
        self,
        style,
        default=None,
    ):
        return self.get_typography(
            style,
            "font_size",
            default,
        )

    def line_height(
        self,
        style,
        default=None,
    ):
        return self.get_typography(
            style,
            "line_height",
            default,
        )

    # ========================================================
    # Theme listeners
    # ========================================================

    def bind_theme_change(
        self,
        callback,
    ):
        if (
            callback not in self._theme_listeners
        ):

            self._theme_listeners.append(
                callback
            )

    def unbind_theme_change(
        self,
        callback,
    ):
        if (
            callback in self._theme_listeners
        ):

            self._theme_listeners.remove(
                callback
            )

    def _notify_theme_change(self):
        """
        Notify a COPY of the listener list so listeners can
        safely bind/unbind themselves during notification.
        """

        for callback in self._theme_listeners[:]:

            try:

                callback(
                    self.current_theme
                )

            except Exception as error:

                print(
                    "Theme change listener error:",
                    error,
                )