from __future__ import annotations

import json
import random
from pathlib import Path

from domain import (
    Commission,
    DefenseProcess,
    DiplomaProject,
    Presentation,
    ScientificSupervisor,
    Student,
    Theme,
)

class SessionService:
    def __init__(self, saves_dir: str | Path):
        self.__saves_dir = Path(saves_dir)
        self.__process: DefenseProcess | None = None
        self.__slot: int | None = None

    def has_save(self, slot: int) -> bool:
        return self._slot_path(slot).exists()

    def start_new(
        self,
        slot: int,
        student_name: str,
        student_intelligence: int,
        seed: int | None = None,
    ) -> DefenseProcess:
        self._validate_slot(slot)
        rng = random.Random(seed)

        themes = [
            Theme("Smart recommendation system", 2),
            Theme("Neural network optimization", 3),
            Theme("Knowledge base assistant", 1),
        ]
        supervisors = ["Dr. Ivanov", "Dr. Petrov", "Dr. Sidorov"]

        student = Student(
            name=student_name,
            intelligence=student_intelligence,
            stamina=80,
            answer_skill=0,
        )
        diploma = DiplomaProject(
            pct_complition=0,
            quality=90,
            theme=rng.choice(themes),
        )
        presentation = Presentation(pct_complition=0)
        supervisor = ScientificSupervisor(
            name=rng.choice(supervisors),
            intelligence=rng.randint(1, 3),
            loyalty=rng.randint(1, 3),
        )
        commission = Commission(loyalty=rng.randint(1, 3))

        process = DefenseProcess(
            student=student,
            diploma_project=diploma,
            presentation=presentation,
            scientific_supervisor=supervisor,
            commission=commission,
            seed=seed,
        )
        self.__process = process
        self.__slot = slot
        self.save()
        return process

    def load(self, slot: int) -> DefenseProcess:
        self._validate_slot(slot)
        slot_path = self._slot_path(slot)
        if not slot_path.exists():
            raise FileNotFoundError(f"Save slot {slot} does not exist.")

        payload = json.loads(slot_path.read_text(encoding="utf-8"))
        process_data = payload.get("process")
        if not isinstance(process_data, dict):
            raise ValueError("Corrupted save file: missing process data.")

        process = DefenseProcess.from_dict(process_data)
        self.__process = process
        self.__slot = slot
        return process

    def save(self) -> Path:
        process = self._require_process()
        slot = self._require_slot()
        self.__saves_dir.mkdir(parents=True, exist_ok=True)

        path = self._slot_path(slot)
        tmp_path = path.with_suffix(".tmp")
        payload = {"slot": slot, "process": process.to_dict()}
        tmp_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        tmp_path.replace(path)
        return path

    def get_status(self) -> dict[str, int | str | bool]:
        return self._require_process().get_status()

    def get_available_actions(self) -> list[str]:
        return self._require_process().get_available_actions()

    def get_action_label(self, action_code: str) -> str:
        return self._require_process().get_action_label(action_code)

    def perform_action(self, action_code: str) -> None:
        process = self._require_process()
        result = process.perform_action(action_code)
        self.save()
        return result

    def is_finished(self) -> bool:
        return self._require_process().is_finished()

    # def get_final_report(self) -> dict[str, int] | None:
    #     return self._require_process().get_final_report()

    def _slot_path(self, slot: int) -> Path:
        return self.__saves_dir / f"slot_{slot}.json"

    @staticmethod
    def _validate_slot(slot: int) -> None:
        if slot <= 0:
            raise ValueError("Slot number must be >= 1.")

    def _require_process(self) -> DefenseProcess:
        if self.__process is None:
            raise RuntimeError("No active session. Start or load a session first.")
        return self.__process

    def _require_slot(self) -> int:
        if self.__slot is None:
            raise RuntimeError("No active slot. Start or load a session first.")
        return self.__slot

