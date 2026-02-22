from __future__ import annotations

import sys
import unittest
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from domain import (
    Commission,
    DefenseProcess,
    DefenseStage,
    DiplomaProject,
    Presentation,
    ScientificSupervisor,
    Student,
    Theme,
)


def make_process(
    *,
    intelligence: int = 2,
    stamina: int = 80,
    answer_skill: int = 0,
    diploma_pct: int = 0,
    diploma_quality: int = 90,
    presentation_pct: int = 0,
    supervisor_intelligence: int = 2,
    supervisor_loyalty: int = 2,
    commission_loyalty: int = 2,
    today: int = 0,
    stage: DefenseStage = DefenseStage.PREPARATION,
) -> DefenseProcess:
    student = Student(
        name="Alice",
        intelligence=intelligence,
        stamina=stamina,
        answer_skill=answer_skill,
    )
    theme = Theme(name="Knowledge base assistant", complexity=2)
    diploma = DiplomaProject(
        pct_complition=diploma_pct,
        quality=diploma_quality,
        theme=theme,
    )
    presentation = Presentation(pct_complition=presentation_pct)
    supervisor = ScientificSupervisor(
        name="Dr. Test",
        intelligence=supervisor_intelligence,
        loyalty=supervisor_loyalty,
    )
    commission = Commission(loyalty=commission_loyalty)
    return DefenseProcess(
        student=student,
        diploma_project=diploma,
        presentation=presentation,
        scientific_supervisor=supervisor,
        commission=commission,
        today=today,
        stage=stage,
        seed=42,
    )


class DefenseProcessTests(unittest.TestCase):
    def test_available_actions_for_each_stage(self) -> None:
        expected = {
            DefenseStage.PREPARATION: ["work_thesis", "rest", "send_review"],
            DefenseStage.REVISION: ["work_thesis", "rest", "submit_for_inspection"],
            DefenseStage.REHEARSAL: ["prepare_slides", "rest", "rehearse"],
            DefenseStage.DEFENSE: ["prepare_slides", "rest", "rehearse", "defense"],
            DefenseStage.ATTESTATION: ["attestation"],
            DefenseStage.FINISHED: [],
        }

        for stage, actions in expected.items():
            with self.subTest(stage=stage):
                process = make_process(stage=stage)
                self.assertEqual(process.get_available_actions(), actions)

    def test_perform_action_rejects_unavailable_action(self) -> None:
        process = make_process(stage=DefenseStage.ATTESTATION)
        with self.assertRaises(ValueError):
            process.perform_action("rest")

    def test_work_thesis_changes_stats(self) -> None:
        process = make_process(
            intelligence=2,
            stamina=80,
            diploma_pct=0,
            diploma_quality=90,
        )

        process.perform_action("work_thesis")
        status = process.get_status()

        self.assertEqual(status["today"], 1)
        self.assertEqual(status["stamina"], 60)
        self.assertEqual(status["thesis_completion"], 20)
        self.assertEqual(status["thesis_quality"], 89)

    def test_submit_for_inspection_marks_all_revisions(self) -> None:
        process = make_process(
            diploma_pct=100,
            today=5,
            stage=DefenseStage.REVISION,
        )

        process.perform_action("submit_for_inspection")
        status = process.get_status()

        self.assertEqual(status["revision_passed"], [True, True, True])
        self.assertEqual(status["final_grade"], 3)
        self.assertEqual(status["score"], 15)
        self.assertEqual(status["stamina"], 73)
        self.assertEqual(status["today"], 6)
        self.assertEqual(status["stage"], DefenseStage.PREPARATION.value)

    def test_defense_action_sets_attestation_stage(self) -> None:
        process = make_process(
            intelligence=1,
            answer_skill=1,
            presentation_pct=50,
            commission_loyalty=1,
            today=23,
            stage=DefenseStage.DEFENSE,
        )

        process.perform_action("defense")
        status = process.get_status()

        self.assertTrue(status["defense_passed"])
        self.assertEqual(status["final_grade"], 1)
        self.assertEqual(status["stage"], DefenseStage.ATTESTATION.value)
        self.assertEqual(status["today"], 24)

    def test_attestation_finishes_process(self) -> None:
        process = make_process(
            intelligence=2,
            diploma_quality=88,
            today=24,
            stage=DefenseStage.ATTESTATION,
        )
        process._DefenseProcess__final_grade = 3
        process._DefenseProcess__score = 10

        process.perform_action("attestation")
        status = process.get_status()

        self.assertEqual(status["final_grade"], 5)
        self.assertEqual(status["score"], 40)
        self.assertEqual(status["today"], 25)
        self.assertTrue(process.is_finished())

    def test_to_dict_from_dict_roundtrip_preserves_state(self) -> None:
        process = make_process(diploma_pct=100, today=5, stage=DefenseStage.REVISION)
        process.perform_action("submit_for_inspection")

        serialized = process.to_dict()
        restored = DefenseProcess.from_dict(serialized)

        self.assertEqual(restored.to_dict(), serialized)


if __name__ == "__main__":
    unittest.main()
