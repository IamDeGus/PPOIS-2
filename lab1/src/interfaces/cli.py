from application import SessionService

from rich.console import Console, Group
from rich.columns import Columns
from rich.panel import Panel
from rich.progress_bar import ProgressBar
from rich.align import Align
from rich.table import Table
from rich.text import Text
from rich.markdown import Markdown

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
    console.print(render_ui(service))
    
    while True:
        console.clear()
        console.print(render_ui(service))

        if service.is_finished():
            console.print(render_final_report(service))
            print("\nSession is finished.")
            break

        action_code = _choose_action(service, console)
        if action_code == "exit":
            save_path = service.save()
            print(f"\nSession saved to {save_path}.")
            break

        service.perform_action(action_code)
        
        
    
        

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

def render_ui(service: SessionService) -> Group:
    status = service.get_status()
    
    # # ----- HEADER -----
    # header_text = f"Day: {status['today']}/{status['max_days']}     Stage: {status['stage']}"
    # header_panel = Panel(header_text,  style="bold cyan", width=53)

    # ----- Student -----
    student_table = Table.grid(expand=True)
    student_table.add_column(no_wrap=True)
    student_table.add_column(ratio=1)
    student_table.add_row()
    student_table.add_row(
        "Name: ", 
        Text(f' {str(status["student_name"])}', style='bold black on white'),
        " ",
        "         "
    )
    student_table.add_row()
    student_table.add_row(
        "Intelligence: ",
        ProgressBar(
            total=3,
            completed=int(status["student_intelligence"]), 
            width=24,
            complete_style="yellow",
            finished_style="yellow",
        ),
        " ",
        Text(
            f" {status['student_intelligence']}/3 ", 
            style=f"bold black on yellow"
        )
    )
    student_table.add_row(
        "Stamina: ",
        ProgressBar(
            total=100, 
            completed=int(status["stamina"]), 
            width=24,
            complete_style="red",
            finished_style="green",
        ),
        " ",
        Text(
            f" {status['stamina']}/100 ", 
            style=f"bold black on {'red' if status['stamina'] != 100 else 'green'}"
        )
    )
    student_table.add_row(
        "Answer skill: ",
        ProgressBar(
            total=3, 
            completed=int(status["answer_skill"]), 
            width=24,
            complete_style="red",
            finished_style="green",
        ),
        " ",
        Text(
            f" {status['answer_skill']}/3 ", 
            style=f"bold black on {'red' if status['answer_skill'] != 3 else 'green'}"
        )
    )
    student_table.add_row()
    student_panel = Panel(student_table, title="Student")


    # ----- Diplom Project -----
    project_table = Table.grid(expand=True)
    project_table.add_column(no_wrap=True)
    project_table.add_column(ratio=1)
    project_table.add_row()
    project_table.add_row(
        "Theme: ", 
        Text(f' {str(status["theme_name"])}', style='bold black on white'),
        " ",
        "         "
    )
    project_table.add_row()
    project_table.add_row(
        "Thesis done: ",
        ProgressBar(
            total=100, 
            completed=int(status["thesis_completion"]), 
            width=31,
            complete_style="red",
            finished_style="green",
        ),
        " ",
        Text(
            f" {status['thesis_completion']}/100 ", 
            style=f"bold black on {'red' if status['thesis_completion'] != 100 else 'green'}"
        )
    )
    project_table.add_row(
        "Quality: ",
        ProgressBar(
            total=100, 
            completed=int(status["thesis_quality"]), 
            width=31,
            complete_style="red",
            finished_style="green",
        ),
        " ",
        Text(
            f" {status['thesis_quality']}/100 ", 
            style=f"bold black on {'red' if status['thesis_quality'] != 100 else 'green'}"
        )
    )
    project_table.add_row(
        "Presentation: ",
        ProgressBar(
            total=100, 
            completed=int(status["presentation"]), 
            width=31,
            complete_style="red",
            finished_style="green",
        ),
        " ",
        Text(
            f" {status['presentation']}/100 ", 
            style=f"bold black on {'red' if status['presentation'] != 100 else 'green'}"
        )
    )
    project_table.add_row()
    project_panel = Panel(project_table, title="Thesis")

    main_columns = Columns([student_panel, project_panel], equal=True)

    # ----- TIMELINE -----
    timeline_table = Table.grid(expand=True)
    timeline_table.add_column(no_wrap=True)
    timeline_table.add_column(ratio=1)
    timeline_table.add_row(
        Columns(
            [
                ProgressBar(
                    total=2.5, 
                    completed=status['today'], 
                    width=6,
                    complete_style="green",
                    finished_style="green",
                ),
                Text("󰷈", style=f"{'green' if status['today'] > 2.5  else 'grey23'}"),
                ProgressBar(
                    total=2.5, 
                    completed=status['today'] - 2.5, 
                    width=6,
                    complete_style="green",
                    finished_style="green",
                ),
                Text(">"),
                
                ProgressBar(
                    total=1, 
                    completed=status['today'] - 5, 
                    width=2,
                    complete_style="green",
                    finished_style="green",
                ),
                Text("󰃯", style=f"{'green' if status['today'] > 6  else 'grey23'}"),
                ProgressBar(
                    total=1, 
                    completed=status['today'] - 6, 
                    width=2,
                    complete_style="green",
                    finished_style="green",
                ),
                Text(">"),
                
                ProgressBar(
                    total=2, 
                    completed=status['today'] - 7, 
                    width=5,
                    complete_style="green",
                    finished_style="green",
                ),
                Text("󰷈", style=f"{'green' if status['today'] > 9  else 'grey23'}"),
                ProgressBar(
                    total=2, 
                    completed=status['today'] - 9, 
                    width=5,
                    complete_style="green",
                    finished_style="green",
                ),
                Text(">"),

                ProgressBar(
                    total=1, 
                    completed=status['today'] - 11,
                    width=2,
                    complete_style="green",
                    finished_style="green",
                ),
                Text("󰃯", style=f"{'green' if status['today'] > 12  else 'grey23'}"),
                ProgressBar(
                    total=1, 
                    completed=status['today'] - 12, 
                    width=2,
                    complete_style="green",
                    finished_style="green",
                ),
                Text(">"),

                ProgressBar(
                    total=1.5, 
                    completed=status['today'] - 13,
                    width=4,
                    complete_style="green",
                    finished_style="green",
                ),
                Text("󰷈", style=f"{'green' if status['today'] > 14.5  else 'grey23'}"),
                ProgressBar(
                    total=1.5, 
                    completed=status['today'] - 14.5, 
                    width=4,
                    complete_style="green",
                    finished_style="green",
                ),
                Text(">"),

                ProgressBar(
                    total=1, 
                    completed=status['today'] - 16,
                    width=2,
                    complete_style="green",
                    finished_style="green",
                ),
                Text("󰃯", style=f"{'green' if status['today'] > 17  else 'grey23'}"),
                ProgressBar(
                    total=1, 
                    completed=status['today'] - 17,
                    width=2,
                    complete_style="green",
                    finished_style="green",
                ),
                Text(">"),

                ProgressBar(
                    total=2.5, 
                    completed=status['today'] - 18,
                    width=6,
                    complete_style="green",
                    finished_style="green",
                ),
                Text("󱆿", style=f"{'green' if status['today'] > 20.5  else 'grey23'}"),
                ProgressBar(
                    total=2.5, 
                    completed=status['today'] - 20.5, 
                    width=6,
                    complete_style="green",
                    finished_style="green",
                ),
                Text(">"),

                ProgressBar(
                    total=1, 
                    completed=status['today'] - 23,
                    width=2,
                    complete_style="green",
                    finished_style="green",
                ),
                Text("󰞀", style=f"{'green' if status['today'] > 24  else 'grey23'}"),
                ProgressBar(
                    total=1, 
                    completed=status['today'] - 24, 
                    width=2,
                    complete_style="green",
                    finished_style="green",
                ),
                Text(">"),

                ProgressBar(
                    total=1, 
                    completed=status['today'] - 24,
                    width=2,
                    complete_style="green",
                    finished_style="green",
                ),
            ]
        )
    )
    
    timeline_panel = Panel(timeline_table, width=112)

    # ----- ACTIONS -----
    actions = service.get_available_actions()
    
    action_tables = Table.grid(expand=True)
    action_tables.add_column(no_wrap=True)
    action_tables.add_column(ratio=1)
    action_tables.add_row()
    
    for idx, action_code in enumerate(actions, start=1):
        action_tables.add_row(
            Text(f"{idx}. "),
            Text(f"{service.get_action_label(action_code)}"),
            Text(service.get_action_help(action_code), style="italic")
        )
    
    action_tables.add_row(Text("0. "), Text("Exit and save   "))
    action_tables.add_row()

    
    actions_panel = Panel(action_tables, title="Actions", width=60)

    return Group(main_columns, timeline_panel, actions_panel)


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


# def _print_status(status: dict[str, int | str | bool]) -> None:
#     print("\n" + "=" * 62)
#     print(
#         f"Day {status['today']}/{status['max_days']} | Stage: {status['stage']} | "
#         f"Student: {status['student_name']}"
#     )
#     print(
#         "Thesis: "
#         f"{status['thesis_completion']}% done, "
#         f"quality {status['thesis_quality']} | "
#         f"Presentation: {status['presentation']}%"
#     )
#     print(
#         f"Stamina: {status['stamina']} | "
#         f"Answer skill: {status['answer_skill']} | "
#         # f"Passed inspections: {status['revision_passed_count']}/3"
#     )
#     print(
#         f"Theme: {status['theme_name']} (complexity {status['theme_complexity']}) | "
#         f"Defense passed: {status['defense_passed']}"
#     )
#     print(f"Score: {status['score']}")
#     print("=" * 62)


def _choose_action(service: SessionService, console: Console) -> str:
    actions = service.get_available_actions()
    status = service.get_status()
    #     header_text = f"Day: {status['today']}/{status['max_days']}     Stage: {status['stage']}"
    # header_panel = Panel(header_text,  style="bold cyan", width=53)
    root_str = f"({status['today']}/{status['max_days']}), {status['stage']}"
    while True:
        raw = console.input(f"[[italic]{root_str}[/]][bold]> [/]").strip()
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


def render_final_report(service: SessionService) -> Group:
    report = service.get_status()

    stata_table = Table.grid(expand=True)
    stata_table.add_column(no_wrap=True)
    stata_table.add_column(ratio=1)
    stata_table.add_row()
    
    if report['defense_passed']:
        stata_table.add_row(
            Text('Final grade:  ', style='bold'),
            Text(f'{report['final_grade']}', style='cyan italic') 
        )
    else:
        stata_table.add_row(
            Text('Final grade:  ', style='bold'),
            Text('LOSE', style='cyan italic')
        )
        
    stata_table.add_row(
        Text('Total score:  ', style='bold'),
        Text(f'{report['score']}', style='cyan italic')
    )
    stata_table.add_row(
        Text('Finished on day:  ', style='bold'),
        Text(f'{report['today']}', style='cyan italic')
    )
    stata_table.add_row()

    stata_panel = Panel(stata_table, width=30)

    return Group(stata_panel)
