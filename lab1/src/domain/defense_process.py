from __future__ import annotations

from .student import Student
from .diploma_project import DiplomaProject
from .presentation import Presentation
from .scientific_supervisor import ScientificSupervisor
from .commission import Commission
from .theme import Theme

from enum import Enum
import random
import ast


class DefenseStage(Enum):
    PREPARATION = "Preparation"
    REVISION = "Revision"
    REHEARSAL = "Rehearsal"
    DEFENSE = "Defense"
    ATTESTATION = "Attestation"
    FINISHED = "Finished"


class DefenseProcess:
    MAX_DAY = 25
    MAX_GRADE = 10

    ACTION_LABELS: dict[str, str] = {
        "work_thesis": "Work on thesis",
        "rest": "Rest",
        "send_review": "Send for review",
        "submit_for_inspection": "Submit for inspection",
        "prepare_slides": "Prepare presentation",
        "rehearse": "Rehearse defense",
        "defense": "Go to defense",
        "attestation": "Get final grade",
    }

    def __init__(
            self,
            student: Student,
            diploma_project: DiplomaProject,
            presentation: Presentation,
            scientific_supervisor: ScientificSupervisor,
            commission: Commission,
            today: int = 0,
            stage: DefenseStage = DefenseStage.PREPARATION,
            seed: int | None = None):

        self.__student: Student = student
        self.__diploma_project: DiplomaProject = diploma_project
        self.__presentation: Presentation = presentation
        self.__scientific_supervisor: ScientificSupervisor = scientific_supervisor
        self.__commission: Commission = commission
        self.__today: int = today
        self.__stage: DefenseStage = stage
        self.__seed: int = seed

        self.__revision_passed: list[bool] = [False, False, False]
        self.__defense_passed: bool = False
        self.__final_grade: int = 0
        self.__score: int = 0

        self.__rng = random.Random(seed)

    def get_action_label(self, action_code: str) -> str:
        return self.ACTION_LABELS[action_code]

    def get_available_actions(self) -> list[str]:
        if self.__stage == DefenseStage.PREPARATION:
            return ['work_thesis', 'rest', 'send_review']
        if self.__stage == DefenseStage.REVISION:
            return ['work_thesis', 'rest', 'submit_for_inspection']
        if self.__stage == DefenseStage.REHEARSAL:
            return ['prepare_slides', 'rest', 'rehearse']
        if self.__stage == DefenseStage.DEFENSE:
            return ['prepare_slides', 'rest', 'rehearse', 'defense']
        if self.__stage == DefenseStage.ATTESTATION:
            return ['attestation']
        return []

    def is_finished(self) -> bool:
        return self.__stage == DefenseStage.FINISHED

    def get_status(self) -> dict[str, int | str | bool]:
        return {
            'today': self.__today,
            'max_days': self.__class__.MAX_DAY,
            'stage': self.__stage.value,
            'student_name': self.__student.get_name(),
            'student_intelligence': self.__student.get_intelligence(),
            'stamina': self.__student.get_stamina(),
            'thesis_completion': self.__diploma_project.get_pct_complition(),
            'thesis_quality': self.__diploma_project.get_quality(),
            'theme_name': self.__diploma_project.get_theme_name(),
            'theme_complexity': self.__diploma_project.get_theme_complexity(),
            'presentation': self.__presentation.get_pct_complition(),
            'answer_skill': self.__student.get_answer_skill(),
            'revision_passed': self.__revision_passed,
            'defense_passed': self.__defense_passed,
            'score': self.__score,
            'final_grade': self.__final_grade
            
        }

    def perform_action(self, action_code: str) -> None:
        if action_code not in self.get_available_actions():
            raise ValueError("Action is not available at the current stage.")

        action_map = {
            'work_thesis': self._work_on_thesis,
            'prepare_slides': self._prepare_slides,
            'rest': self._rest,
            'send_review': self._send_to_review,
            'submit_for_inspection': self._submit_for_inspection,
            'rehearse': self._rehearse_defense,
            'defense': self._start_defense,
            'attestation': self._perform_attestation,
        }
        return action_map[action_code]()

    def change_day(self) -> None:
        if self.__today < self.__class__.MAX_DAY:
            self.__today += 1

        if self.__today in (5, 11, 16):
            self.__stage = DefenseStage.REVISION
            
        if (self.__today in (6, 7, 12, 13) and
            self.__revision_passed[self.__today // 8] == True):
            self.__stage = DefenseStage.PREPARATION
            
        if (self.__today in (17, 18) and
            self.__revision_passed[2] == True):
            self.__stage = DefenseStage.REHEARSAL
            
        if (self.__today in (7, 13, 18) and
            self.__revision_passed[self.__today // 8] == False):
            self.__stage = DefenseStage.FINISHED
        
        if self.__today in (24, 23):
            self.__stage = DefenseStage.DEFENSE

        if (self.__stage == DefenseStage.ATTESTATION):
            self.__stage = DefenseStage.FINISHED
        elif (self.__today == 25 or self.__defense_passed == True):
            self.__stage = DefenseStage.ATTESTATION

        return True
    
    def _work_on_thesis(self) -> None:
        k1: int = self.__student.get_intelligence() - 2  
        k2: int = 5 - self.__student.get_stamina() // 20
        
        self.__student.change_stamina(-20)
        self.__diploma_project.change_complition(22 + k1 * 2 - k2 * 2)
        self.__diploma_project.change_quality(k1 - k2)
        
        self.change_day()
            
    def _prepare_slides(self) -> None:
        k1: int = self.__student.get_intelligence() - 2  
        k2: int = 5 - self.__student.get_stamina() // 20
        
        self.__student.change_stamina(-15)
        self.__presentation.change_complition(52 + k1 * 2 - k2 * 2)
        
        self.change_day()

    def _rest(self) -> None:
        self.__student.change_stamina(20)
        
        self.__score += 9
        
        self.change_day()
        
    def _send_to_review(self) -> None:
        k = (self.__scientific_supervisor.get_intelligence()
             - self.__student.get_intelligence())
        
        self.__student.change_stamina(-10)
        self.__diploma_project.change_quality(
            (k + self.__scientific_supervisor.get_loyalty()) * 4)
        
        self.__score -= 3
        
        self.change_day()
        
    def _submit_for_inspection(self) -> None:
        pct: int = self.__diploma_project.get_pct_complition()
        if (pct > 33 and self.__revision_passed[0] == False):
            self.__revision_passed[0] = True
            self.__final_grade += 1 - self.__today // 6
            self.__score += 2
        if (pct > 66 and self.__revision_passed[1] == False):
            self.__revision_passed[1] = True
            self.__final_grade += 1 - self.__today // 12
            self.__score += 5
        if (pct == 100 and self.__revision_passed[2] == False):
            self.__revision_passed[2] = True
            self.__final_grade += 1 - self.__today // 17
            self.__score += 8
        
        self.__student.change_stamina(-7)
        
        self.change_day()
        
    def _rehearse_defense(self) -> None:
        self.__student.change_answer_skill(self.__student.get_stamina() // 50)
        self.__student.change_stamina(-15)
        
        self.change_day()
        
    def _start_defense(self) -> None:
        self.__defense_passed = True
        self.__student.change_stamina(-20)
        self.__final_grade += (1 + self.__student.get_answer_skill())
        
        if (self.__commission.get_loyalty() 
            + self.__student.get_intelligence() <= 3 or
            self.__presentation.get_pct_complition() <= 51):
            self.__final_grade -= 1
        
        self.change_day()
        
        
    def _perform_attestation(self) -> None:
        self.__final_grade += (self.__diploma_project.get_quality() - 70) // 9
        
        self.__score += self.__final_grade * 2
        self.__score *= (4 - self.__student.get_intelligence())
        self.change_day()


    def to_dict(self) -> dict[str, object]:
        return {
            'today': self.__today,
            'stage': self.__stage.name,
            'seed': self.__seed,
            'revision_passed': self.__revision_passed,
            'defense_passed': self.__defense_passed,
            'final_grade': self.__final_grade,
            'score': self.__score,
            'student': {
                'name': self.__student.get_name(),
                'intelligence': self.__student.get_intelligence(),
                'stamina': self.__student.get_stamina(),
                'answer_skill': self.__student.get_answer_skill(),
            },
            'theme': {
                'name': self.__diploma_project.get_theme_name(),
                'complexity': self.__diploma_project.get_theme_complexity(),
            },
            'diploma_project': {
                'pct_complition': self.__diploma_project.get_pct_complition(),
                'quality': self.__diploma_project.get_quality(),
            },
            'presentation': {
                'pct_complition': self.__presentation.get_pct_complition(),
            },
            'supervisor': {
                'name': self.__scientific_supervisor.get_name(),
                'intelligence': self.__scientific_supervisor.get_intelligence(),
                'loyalty': self.__scientific_supervisor.get_loyalty(),
            },
            'commission': {
                'loyalty': self.__commission.get_loyalty(),
            }
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> DefenseProcess:
        student_data = data["student"]
        theme_data = data["theme"]
        diploma_data = data["diploma_project"]
        presentation_data = data["presentation"]
        supervisor_data = data["supervisor"]
        commission_data = data["commission"]
        
        
        theme = Theme(
            name=str(theme_data["name"]),
            complexity=int(theme_data["complexity"]),
        )
        student = Student(
            name=str(student_data["name"]),
            intelligence=int(student_data["intelligence"]),
            stamina=int(student_data["stamina"]),
            answer_skill=int(student_data["answer_skill"]),
        )
        diploma_project = DiplomaProject(
            pct_complition=int(diploma_data["pct_complition"]),
            quality=int(diploma_data["quality"]),
            theme=theme,
        )
        presentation = Presentation(
            pct_complition=int(presentation_data["pct_complition"]),
        )
        supervisor = ScientificSupervisor(
            name=str(supervisor_data["name"]),
            intelligence=int(supervisor_data["intelligence"]),
            loyalty=int(supervisor_data["loyalty"]),
        )
        commission = Commission(loyalty=int(commission_data["loyalty"]))

        stage_name = str(data["stage"])
        process = cls(
            student=student,
            diploma_project=diploma_project,
            presentation=presentation,
            scientific_supervisor=supervisor,
            commission=commission,
            today=int(data["today"]),
            stage=DefenseStage[stage_name],
            seed=data.get("seed"),
        )

        revision_passed = data["revision_passed"]
        final_grade = data["final_grade"]
        
        process.__revision_passed = [bool(item) for item in revision_passed]
        process.__defense_passed = bool(data.get("defense_passed", False))
        
        
        
        process.__final_grade = int(final_grade) if final_grade is not None else None
        process.__score = int(data["score"])

        rng_state = data["seed"]
        
        if isinstance(rng_state, str):
            process.__rng.setstate(ast.literal_eval(rng_state))

        return process
