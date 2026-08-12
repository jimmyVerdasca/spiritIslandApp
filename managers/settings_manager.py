import json
import os


class SettingsManager:

    DEFAULT_SETTINGS = {
        "language": "en",
        "theme": "dark",
    }

    def __init__(self):

        self.file_path = "data/user_settings.json"

        self.settings = self.load()

    # --------------------------------------------------
    # Load
    # --------------------------------------------------

    def load(self):

        # If no settings file exists yet,
        # create one with the default values.
        if not os.path.exists(self.file_path):

            self.save(
                self.DEFAULT_SETTINGS.copy()
            )

            return self.DEFAULT_SETTINGS.copy()

        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8",
            ) as file:

                settings = json.load(file)

        except (
            json.JSONDecodeError,
            OSError,
        ):

            settings = self.DEFAULT_SETTINGS.copy()

        # Ensure new default settings are added
        # if you add more settings later.
        for key, value in self.DEFAULT_SETTINGS.items():

            settings.setdefault(
                key,
                value,
            )

        return settings

    # --------------------------------------------------
    # Save
    # --------------------------------------------------

    def save(self, settings=None):

        if settings is not None:

            self.settings = settings

        os.makedirs(
            os.path.dirname(self.file_path),
            exist_ok=True,
        )

        with open(
            self.file_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self.settings,
                file,
                indent=4,
                ensure_ascii=False,
            )

    # --------------------------------------------------
    # Get
    # --------------------------------------------------

    def get(self, key):

        return self.settings.get(
            key,
            self.DEFAULT_SETTINGS.get(key),
        )

    # --------------------------------------------------
    # Set
    # --------------------------------------------------

    def set(self, key, value):

        self.settings[key] = value

        self.save()