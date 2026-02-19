from __future__ import annotations

import sys
import unittest
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from domain import Student


class StudentTests(unittest.TestCase):
    def test_init_rejects_empty_name(self) -> None:
        with self.assertRaises(ValueError):
            Student(name="", intelligence=2)

    def test_init_rejects_invalid_intelligence(self) -> None:
        with self.assertRaises(ValueError):
            Student(name="Alice", intelligence=4)

    def test_change_stamina_is_clamped_to_range(self) -> None:
        student = Student(name="Alice", intelligence=2, stamina=90)

        student.change_stamina(50)
        self.assertEqual(student.get_stamina(), 100)

        student.change_stamina(-200)
        self.assertEqual(student.get_stamina(), 0)

    def test_change_answer_skill_is_clamped_to_max(self) -> None:
        student = Student(name="Alice", intelligence=2, answer_skill=1)

        student.change_answer_skill(10)
        self.assertEqual(student.get_answer_skill(), 3)

    def test_get_str_intelligence_mapping(self) -> None:
        self.assertEqual(Student("A", 1).get_str_intelligence(), "low")
        self.assertEqual(Student("A", 2).get_str_intelligence(), "middle")
        self.assertEqual(Student("A", 3).get_str_intelligence(), "high")


if __name__ == "__main__":
    unittest.main()
