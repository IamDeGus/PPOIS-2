from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from application import SessionService


class SessionServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.saves_dir = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_start_new_creates_save_file(self) -> None:
        service = SessionService(self.saves_dir)

        service.start_new(
            slot=1,
            student_name="Alice",
            student_intelligence=2,
            seed=123,
        )

        slot_path = self.saves_dir / "slot_1.json"
        self.assertTrue(slot_path.exists())
        self.assertTrue(service.has_save(1))

        payload = json.loads(slot_path.read_text(encoding="utf-8"))
        self.assertEqual(payload["slot"], 1)
        self.assertIn("process", payload)

    def test_load_restores_existing_session(self) -> None:
        first_service = SessionService(self.saves_dir)
        first_service.start_new(
            slot=1,
            student_name="Alice",
            student_intelligence=2,
            seed=123,
        )

        second_service = SessionService(self.saves_dir)
        second_service.load(1)
        status = second_service.get_status()

        self.assertEqual(status["student_name"], "Alice")
        self.assertEqual(status["student_intelligence"], 2)

    def test_load_missing_slot_raises(self) -> None:
        service = SessionService(self.saves_dir)
        with self.assertRaises(FileNotFoundError):
            service.load(99)

    def test_start_new_rejects_invalid_slot(self) -> None:
        service = SessionService(self.saves_dir)
        with self.assertRaises(ValueError):
            service.start_new(
                slot=0,
                student_name="Alice",
                student_intelligence=2,
                seed=1,
            )

    def test_perform_action_without_active_session_raises(self) -> None:
        service = SessionService(self.saves_dir)
        with self.assertRaises(RuntimeError):
            service.perform_action("rest")

    def test_perform_action_updates_saved_state(self) -> None:
        service = SessionService(self.saves_dir)
        service.start_new(
            slot=1,
            student_name="Alice",
            student_intelligence=2,
            seed=123,
        )

        service.perform_action("rest")

        payload = json.loads((self.saves_dir / "slot_1.json").read_text(encoding="utf-8"))
        process_data = payload["process"]
        self.assertEqual(process_data["today"], 1)
        self.assertEqual(process_data["student"]["stamina"], 100)


if __name__ == "__main__":
    unittest.main()
