from application import SessionService

from rich.console import Console
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.progress_bar import ProgressBar
from rich.align import Align
import time

def run_cli(
    service: SessionService,
    slot: int,
    create_new: bool = False,
    seed: int | None = None,
) -> None:
    if create_new or not service.has_save(slot):
        
        print(f"Starting new session in slot {slot}.")
        student_name = input("Student name: ").strip() or "Anonymous Student"
        student_intelligence = _prompt_int("Student intelligence (1..3): ", 1, 3)
        service.start_new(
            slot=slot,
            student_name=student_name,
            student_intelligence=student_intelligence,
            seed=seed,
        )
    else:
        service.load(slot)
        print(f"Loaded existing session from slot {slot}.")


    console = Console()
    table_1 = Table(show_footer=False)
    column_text = 'Day:   Stage:  '
    column = Panel(column_text)
    # table_3
    # table_4
    # print(column)
    table_centered = Align.center(table_1)
    
    with Live(Panel(column_text), console=console, screen=False, refresh_per_second=20) as live:
        column_text = 'opaopaopaopa'
        time.sleep(5)
        live.update(Panel(column_text))

    time.sleep(5)

    
        

    # while True:
    #     console = Console()
    #     table = Table(show_footer=False)
    #     table_centered = Align.center(table)
        
        
    #     _print_status(service.get_status())

    #     if service.is_finished():
    #         print("\nSession is finished.")
    #         _print_final_report(service)
    #         break

    #     action_code = _choose_action(service)
    #     if action_code == "exit":
    #         save_path = service.save()
    #         print(f"\nSession saved to {save_path}.")
    #         break

    #     result = service.perform_action(action_code)
    #     # print(f"\n[Result] {result.message}")

    #     # if result.stage_changed and not result.finished:
    #     #     print("Stage changed.")

def render_ui(status: dict[str, int | str | bool]) -> La:

    layout = Layout()

    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main", ratio=3),
        Layout(name="timeline", size=3),
        Layout(name="actions", size=6),
        Layout(name="input", size=3),
    )

    # ----- HEADER -----
    header_text = f"Day: {status['today']}/{status['max_days']}     Stage: {status['stage']}"
    layout["header"].update(Panel(header_text, style="bold cyan"))

    # ----- MAIN COLUMNS -----
    main_table = Table.grid(expand=True)
    main_table.add_column()
    main_table.add_column()

    student_panel = Panel(
        f"""
Name: {status['student_name']}
Intelligence: {status['student_intelligence']}

Стамина:
{ProgressBar(total=100, completed=state.stamina)}

Answer skill:
{ProgressBar(total=100, completed=state.answer_skill)}
        """,
        title="Student",
    )

    project_panel = Panel(
        f"""
Тема: ИИ для анализа данных

Тезис:
{ProgressBar(total=100, completed=state.thesis)}

Качество:
{ProgressBar(total=100, completed=state.quality)}

Презентация:
{ProgressBar(total=100, completed=state.presentation)}
""",
        title="Дипломный проект",
    )

    main_table.add_row(student_panel, project_panel)

    layout["main"].update(main_table)

    # ----- TIMELINE -----
    timeline_bar = ProgressBar(total=25, completed=state.day)
    layout["timeline"].update(
        Panel(Align.center(timeline_bar), title="Временная линия")
    )

    # ----- ACTIONS -----
    actions = Panel(
        "1) Учиться\n"
        "2) Писать тезис\n"
        "3) Отдыхать\n",
        title="Действия",
    )

    layout["actions"].update(actions)

    # ----- INPUT PLACE -----
    layout["input"].update(
        Panel("Введите команду...", title="Команда")
    )

    return layout


def _prompt_int(prompt: str, min_value: int, max_value: int) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Please enter a number.")
            continue

        if min_value <= value <= max_value:
            return value

        print(f"Value must be between {min_value} and {max_value}.")


def _print_status(status: dict[str, int | str | bool]) -> None:
    print("\n" + "=" * 62)
    print(
        f"Day {status['today']}/{status['max_days']} | Stage: {status['stage']} | "
        f"Student: {status['student_name']}"
    )
    print(
        "Thesis: "
        f"{status['thesis_completion']}% done, "
        f"quality {status['thesis_quality']} | "
        f"Presentation: {status['presentation']}%"
    )
    print(
        f"Stamina: {status['stamina']} | "
        f"Answer skill: {status['answer_skill']} | "
        # f"Passed inspections: {status['revision_passed_count']}/3"
    )
    print(
        f"Theme: {status['theme_name']} (complexity {status['theme_complexity']}) | "
        f"Defense passed: {status['defense_passed']}"
    )
    print(f"Score: {status['score']}")
    print("=" * 62)


def _choose_action(service: SessionService) -> str:
    actions = service.get_available_actions()
    for idx, action_code in enumerate(actions, start=1):
        print(f"{idx}. {service.get_action_label(action_code)}")
    print("0. Exit and save")

    while True:
        raw = input("> ").strip()
        if raw == "0":
            return "exit"
        try:
            selected = int(raw)
        except ValueError:
            print("Please enter a valid number.")
            continue

        if 1 <= selected <= len(actions):
            return actions[selected - 1]
        print("No such option. Try again.")


def _print_final_report(service: SessionService) -> None:
    report = service.get_status()

    print("-" * 62)
    print(f"Final grade (10): {report['final_grade']}")
    print(f"Total score: {report['score']}")
    print(f"Finished on day: {report['today']}")
    print("-" * 62)
