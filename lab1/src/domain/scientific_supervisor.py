class ScientificSupervisor:
    ALLOWED_INTELLIGENCE: tuple[int, int, int] = (1, 2, 3)
    ALLOWED_LOYALTY: tuple[int, int, int] = (1, 2, 3)

    def __init__(self, name: str, intelligence: int, loyalty: int):
        self._validate_name(name)
        self._validate_intelligence(intelligence)
        self._validate_loyalty(loyalty)

        self.__name: str = name
        self.__intelligence: int = intelligence
        self.__loyalty: int = loyalty

    @staticmethod
    def _validate_name(name: str) -> None:
        if not name:
            raise ValueError("Name must be a non-empty string.")

    @classmethod
    def _validate_intelligence(cls, intelligence: int) -> None:
        if intelligence not in cls.ALLOWED_INTELLIGENCE:
            raise ValueError("Intelligence must be 1, 2 or 3.")

    @classmethod
    def _validate_loyalty(cls, loyalty: int) -> None:
        if loyalty not in cls.ALLOWED_LOYALTY:
            raise ValueError("Loyaltye must be 1, 2 or 3.")

    def get_name(self):
        return self.__name

    def get_intelligence(self):
        return self.__intelligence

    def get_loyalty(self):
        return self.__loyalty
