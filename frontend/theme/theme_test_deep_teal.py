THEMES = {

    "palette": {

        "neutral": {
            "0":   (1.00, 1.00, 1.00, 1),
            "50":  (0.97, 0.98, 0.97, 1),
            "100": (0.92, 0.94, 0.93, 1),
            "200": (0.84, 0.87, 0.86, 1),
            "300": (0.72, 0.76, 0.75, 1),
            "400": (0.58, 0.63, 0.62, 1),
            "500": (0.44, 0.50, 0.49, 1),
            "600": (0.32, 0.39, 0.38, 1),
            "700": (0.23, 0.29, 0.29, 1),
            "800": (0.15, 0.21, 0.21, 1),
            "850": (0.10, 0.16, 0.16, 1),
            "900": (0.06, 0.11, 0.11, 1),
            "950": (0.03, 0.07, 0.07, 1),
        },

        "teal": {
            "100": (0.78, 0.91, 0.89, 1),
            "200": (0.57, 0.82, 0.78, 1),
            "300": (0.38, 0.70, 0.65, 1),
            "400": (0.23, 0.59, 0.55, 1),
            "500": (0.09, 0.46, 0.43, 1),
            "600": (0.06, 0.34, 0.32, 1),
            "700": (0.04, 0.25, 0.24, 1),
            "800": (0.03, 0.17, 0.17, 1),
        },

        "green": {
            "100": (0.84, 0.94, 0.84, 1),
            "200": (0.68, 0.86, 0.68, 1),
            "300": (0.48, 0.74, 0.49, 1),
            "400": (0.30, 0.62, 0.35, 1),
            "500": (0.18, 0.50, 0.25, 1),
            "600": (0.12, 0.39, 0.19, 1),
            "700": (0.08, 0.30, 0.14, 1),
            "800": (0.05, 0.21, 0.10, 1),
        },

        "amber": {
            "100": (1.00, 0.94, 0.72, 1),
            "200": (0.98, 0.82, 0.42, 1),
            "300": (0.94, 0.70, 0.20, 1),
            "400": (0.88, 0.56, 0.08, 1),
            "500": (0.76, 0.43, 0.04, 1),
            "600": (0.58, 0.30, 0.02, 1),
        },

        "red": {
            "100": (1.00, 0.86, 0.84, 1),
            "200": (0.96, 0.68, 0.64, 1),
            "300": (0.88, 0.44, 0.40, 1),
            "400": (0.78, 0.25, 0.22, 1),
            "500": (0.66, 0.14, 0.12, 1),
            "600": (0.50, 0.08, 0.07, 1),
        },

        "blue": {
            "100": (0.82, 0.92, 0.96, 1),
            "200": (0.62, 0.82, 0.90, 1),
            "300": (0.40, 0.67, 0.80, 1),
            "400": (0.25, 0.53, 0.68, 1),
            "500": (0.14, 0.41, 0.56, 1),
            "600": (0.08, 0.29, 0.42, 1),
        },

        "overlay": {
            "black_50": (0.00, 0.00, 0.00, 0.50),
            "black_65": (0.00, 0.00, 0.00, 0.65),
            "black_78": (0.00, 0.00, 0.00, 0.78),
            "black_85": (0.00, 0.00, 0.00, 0.85),
            "white_30": (1.00, 1.00, 1.00, 0.30),
            "white_55": (1.00, 1.00, 1.00, 0.55),
            "white_65": (1.00, 1.00, 1.00, 0.65),
            "white_75": (1.00, 1.00, 1.00, 0.75),
            "white_80": (1.00, 1.00, 1.00, 0.80),
            "white_82": (1.00, 1.00, 1.00, 0.82),
            "white_85": (1.00, 1.00, 1.00, 0.85),
            "white_88": (1.00, 1.00, 1.00, 0.88),
            "transparent": (0.00, 0.00, 0.00, 0.00),
        },
    },

    "dark": {

        "background": "palette.neutral.900",
        "background_overlay": "palette.overlay.black_50",

        "top_bar": "palette.teal.500",
        "top_bar_button": "palette.teal.500",

        "button": "palette.teal.500",
        "button_disabled": "palette.neutral.700",
        "inactive_button": "palette.neutral.700",

        "success": "palette.green.500",
        "defeat": "palette.red.400",
        "warning": "palette.amber.400",
        "selection_warning": "palette.amber.400",

        "card": "palette.overlay.black_85",
        "card_pressed": "palette.neutral.700",
        "card_overlay": "palette.overlay.black_78",
        "card_text_secondary": "palette.overlay.white_65",

        "player_card_text": "palette.neutral.0",

        "trophy_unlocked": "palette.green.800",
        "trophy_locked": "palette.neutral.700",

        "spirit_card": "palette.neutral.900",
        "spirit_card_empty": "palette.neutral.800",
        "spirit_card_pressed": "palette.neutral.700",
        "spirit_name_background": "palette.overlay.black_78",
        "spirit_text": "palette.neutral.0",
        "spirit_empty_text": "palette.neutral.300",

        "text_primary": "palette.neutral.0",
        "text_secondary": "palette.overlay.white_80",
        "text_muted": "palette.overlay.white_55",

        "icon": "palette.neutral.0",

        "progress": "palette.teal.400",

        "selection_selected": "palette.teal.500",
        "selection_normal": "palette.neutral.700",

        "dropdown_background": "palette.neutral.800",
        "dropdown_text": "palette.neutral.0",
        "dropdown_selected": "palette.teal.800",
        "dropdown_text_selected": "palette.teal.300",
        "dropdown_warning": "palette.amber.600",
        "dropdown_text_warning": "palette.amber.200",
    },

    "light": {

        "background": "palette.neutral.100",
        "background_overlay": "palette.overlay.white_30",

        "top_bar": "palette.teal.500",
        "top_bar_button": "palette.teal.500",

        "button": "palette.teal.500",
        "button_disabled": "palette.neutral.300",
        "inactive_button": "palette.neutral.200",

        "success": "palette.green.500",
        "defeat": "palette.red.400",
        "warning": "palette.amber.400",
        "selection_warning": "palette.amber.400",

        "card": "palette.overlay.white_88",
        "card_pressed": "palette.neutral.200",
        "card_overlay": "palette.overlay.white_85",
        "card_text_secondary": "palette.overlay.black_65",

        "player_card_text": "palette.neutral.0",

        "trophy_unlocked": "palette.green.100",
        "trophy_locked": "palette.neutral.300",

        "spirit_card": "palette.neutral.50",
        "spirit_card_empty": "palette.neutral.100",
        "spirit_card_pressed": "palette.neutral.200",
        "spirit_name_background": "palette.overlay.white_82",
        "spirit_text": "palette.neutral.900",
        "spirit_empty_text": "palette.neutral.600",

        "text_primary": "palette.neutral.900",
        "text_secondary": "palette.overlay.black_65",
        "text_muted": "palette.overlay.black_50",

        "icon": "palette.neutral.900",

        "progress": "palette.teal.500",

        "selection_selected": "palette.teal.500",
        "selection_normal": "palette.neutral.200",

        "dropdown_background": "palette.neutral.0",
        "dropdown_text": "palette.neutral.900",
        "dropdown_selected": "palette.teal.100",
        "dropdown_text_selected": "palette.teal.700",
        "dropdown_warning": "palette.amber.100",
        "dropdown_text_warning": "palette.amber.600",
    },

    "dimensions": {
        "spacing": {
            "xs": 4, "sm": 8, "md": 12,
            "lg": 16, "xl": 24, "xxl": 32,
        },
        "screen": {
            "padding": 20,
            "content_spacing": 12,
        },
        "top_bar": {
            "height": 56,
            "horizontal_padding": 16,
            "spacing": 8,
        },
        "card": {
            "height": 80,
            "padding": 16,
            "spacing": 12,
            "radius": 16,
            "border_width": 1,
        },
        "button": {
            "height": 48,
            "radius": 12,
            "horizontal_padding": 16,
        },
        "input": {
            "height": 48,
            "radius": 8,
            "horizontal_padding": 12,
        },
        "selection": {
            "height": 48,
            "radius": 12,
            "horizontal_padding": 12,
        },
        "icon": {
            "small": 18,
            "medium": 24,
            "large": 32,
        },
        "border": {
            "thin": 1,
            "medium": 2,
        },
        "progress": {
            "height": 15,
        },
    },

    "typography": {
        "display": {
            "font_size": 34,
            "line_height": 1.20,
        },
        "title": {
            "font_size": 24,
            "line_height": 1.20,
        },
        "subtitle": {
            "font_size": 18,
            "line_height": 1.30,
        },
        "body": {
            "font_size": 16,
            "line_height": 1.40,
        },
        "secondary": {
            "font_size": 14,
            "line_height": 1.40,
        },
        "caption": {
            "font_size": 12,
            "line_height": 1.30,
        },
        "button": {
            "font_size": 14,
        },
        "input": {
            "font_size": 16,
        },
        "score": {
            "font_size": 20,
            "line_height": 1.20,
        },
    },
}