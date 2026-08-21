from pathlib import Path


class AssetManager:

    ASSETS_DIR = Path(__file__).resolve().parent.parent.joinpath("assets")

    @classmethod
    def path(cls, *parts):
        """
        Return the absolute path to an application asset.
        """

        path = cls.ASSETS_DIR.joinpath(*parts)

        if path.exists():
            return str(path)

        raise FileNotFoundError(
            f"Asset not found: {path}"
        )