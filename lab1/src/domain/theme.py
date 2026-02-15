class Theme:
    ALLOWED_COMLEXITY: tuple[int, int, int] = (1, 2, 3)

    def __init__(self, name: str, complexity: int):
        self._validate_complexity(complexity)
        self._validate_name(name)
    
        self.__name: str = name
        self.__complexity: int = complexity

    @classmethod
    def _validate_complexity(cls, complexity: int) -> None:
        if complexity not in cls.ALLOWED_COMLEXITY:
            raise ValueError("Complexity must be 1, 2 or 3.")

    @staticmethod
    def _validate_name(name: str) -> None:
        if not name:
            raise ValueError("Name must be a non-empty string.")
  
    def get_name(self) -> str:
        return self.__name
    
    def get_complexity(self) -> int:
        return self.__complexity
