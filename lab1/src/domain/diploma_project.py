from .theme import Theme


class DiplomaProject:
    MIN_PCT: int = 0
    MAX_PCT: int = 100

    MIN_QUALITY: int = 0
    MAX_QUALITY: int = 100

    def __init__(self, pct_complition: int, quality: int, theme: Theme):
        self._validate_pct_complition(pct_complition)
        self._validate_quality(quality)

        self.__pct_complition: int = pct_complition
        self.__quality: int = quality
        self.__theme: Theme = theme

    @classmethod
    def _validate_pct_complition(cls, pct_complition: int) -> None:
        if not cls.MIN_PCT <= pct_complition <= cls.MAX_PCT:
            raise ValueError("Pct complition must be between 0 and 100.")

    @classmethod
    def _validate_quality(cls, quality: int) -> None:
        if not cls.MIN_QUALITY <= quality <= cls.MAX_QUALITY:
            raise ValueError("Quality must be between 0 and 100.")

    def get_pct_complition(self) -> int:
        return self.__pct_complition

    def get_quality(self) -> int:
        return self.__quality

    def get_theme_name(self) -> str:
        return self.__theme.get_name()

    def get_theme_complexity(self) -> int:
        return self.__theme.get_complexity()

    def change_complition(self, delta: int) -> int:
        new_pct_complition = self.__pct_complition + delta
        self.__pct_complition = max(self.MIN_PCT, min(
            self.MAX_PCT, new_pct_complition))
        return self.__pct_complition

    def change_quality(self, delta: int) -> int:
        new_quality = self.__quality + delta
        self.__quality = max(self.MIN_QUALITY, min(
            self.MAX_QUALITY, new_quality))
        return self.__quality
