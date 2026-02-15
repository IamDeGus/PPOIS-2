class Presentation:
    MIN_PCT: int = 0
    MAX_PCT: int = 100

    def __init__(self, pct_complition: int = 0):
        self._validate_pct_comlition(pct_complition)

        self.__pct_complition: int = pct_complition

    @classmethod
    def _validate_pct_comlition(cls, pct_complition: int) -> None:
        if not cls.MIN_PCT <= pct_complition <= cls.MAX_PCT:
            raise ValueError("Pct complition must be between 0 and 100.")

    def get_pct_complition(self) -> int:
        return self.__pct_complition

    def change_complition(self, delta: int) -> int:
        new_pct_complition = self.__pct_complition + delta
        self.__pct_complition = max(self.MIN_PCT, min(
            self.MAX_PCT, new_pct_complition))
        return self.__pct_complition
