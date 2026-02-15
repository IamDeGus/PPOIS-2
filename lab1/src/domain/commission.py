class Commission:
    ALLOWED_LOYALTY: tuple[int, int, int] = (1, 2, 3)
    
    def __init__(self, loyalty: int):
        self._validate_loyalty(loyalty)

        self.__loyalty: int = loyalty

    @classmethod
    def _validate_loyalty(cls, loyalty: int) -> None:
        if loyalty not in cls.ALLOWED_LOYALTY:
            raise ValueError("Loyaltye must be 1, 2 or 3.")

    def get_loyalty(self):
        return self.__loyalty
