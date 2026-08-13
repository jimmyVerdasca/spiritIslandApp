from data.translations import TRANSLATIONS


class LanguageManager:

    def __init__(self, language="en"):

        self.current_language = language


    def set_language(self, language):

        self.current_language = language


    def get(self, key, *categories):
    
        value = TRANSLATIONS[
            self.current_language
        ]

        for category in categories:

            value = value.get(
                category,
                {}
            )

        return value.get(
            key,
            key
        )