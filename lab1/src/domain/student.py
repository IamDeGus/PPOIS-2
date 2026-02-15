class Student:
    MIN_STAMINA: int = 0
    MAX_STAMINA: int = 100
    ALLOWED_INTELLIGENCE: tuple[int, int, int] = (1, 2, 3)

    def __init__(self, name: str, intelligence: int, stamina: int = 100):
        self._validate_name(name)
        self._validate_intelligence(intelligence)
        self._validate_stamina(stamina)

        self.__name = name
        self.__intelligence = intelligence
        self.__stamina = stamina

    @staticmethod
    def _validate_name(name: str) -> None:
        if not name:
            raise ValueError("Name must be a non-empty string.")

    @classmethod
    def _validate_stamina(cls, stamina: int) -> None:
        if not cls.MIN_STAMINA <= stamina <= cls.MAX_STAMINA:
            raise ValueError("Stamina must be between 0 and 100.")

    @classmethod
    def _validate_intelligence(cls, intelligence: int) -> None:
        if intelligence not in cls.ALLOWED_INTELLIGENCE:
            raise ValueError("Intelligence must be 1, 2 or 3.")

    def get_name(self) -> str:
        return self.__name

    def get_intelligence(self) -> int:
        return self.__intelligence

    def get_stamina(self) -> int:
        return self.__stamina

    # def get_stats(self) -> dict[str, int | str]:
    #     return {
    #         "name": self.__name,
    #         "intelligence": self.__intelligence,
    #         "stamina": self.__stamina,
    #     }

    def change_stamina(self, delta: int) -> int:
        new_stamina = self.__stamina + delta
        self.__stamina = max(self.MIN_STAMINA, min(
            self.MAX_STAMINA, new_stamina))
        return self.__stamina
