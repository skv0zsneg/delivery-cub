from enum import Enum


class RateMarkEnum(Enum):
    """Перечень значений для оценки"""

    VERY_BAD = (1, "Very bad")
    CAN_BE_BETTER = (2, "Can be better")
    NORMAL = (3, "Normal")
    GOOD = (4, "Good")
    EXCELLENT = (5, "Excellent")

    def __init__(self, grade: int, description: str) -> None:
        self.grade = grade
        self.description = description
