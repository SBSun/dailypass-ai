from enum import Enum


class QuestionDifficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

    @property
    def get_code(self) -> str:
        return self.value