import pathlib

import click
from rich import print

from cfp.assign import (
    assign_reviewers,
    dump_stats,
    filter_assignments_by_proposal,
    filter_assignments_by_reviewer,
)
from cfp.utils import get_assignments, get_reviewers, get_sessions, write_assignments

SESSIONS_FILE = pathlib.Path(__file__).parent.parent / "sessions.csv"
REVIEWERS_FILE = pathlib.Path(__file__).parent.parent / "reviewers.csv"
ASSIGNMENTS_FILE = pathlib.Path(__file__).parent.parent / "assignments.json"


@click.group()
def assignments() -> None:
    pass


@assignments.command("create", help="Generate assignment of reviewers to proposals")
@click.option(
    "--sessions",
    "sessions_file",
    type=click.Path(exists=True, dir_okay=False, readable=True, path_type=pathlib.Path),
    default=SESSIONS_FILE,
    help="Alternative path to a file containing all the session as exported from Pretalx",
)
@click.option(
    "--reviewers",
    "reviewers_file",
    type=click.Path(exists=True, dir_okay=False, readable=True, path_type=pathlib.Path),
    default=REVIEWERS_FILE,
    help="Alternative path to a file containing all the reviewers as exported from Pretalx",
)
@click.option(
    "--regen",
    is_flag=True,
    help="Regenerate the assignments even if they already exist",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Print additional information about the assignments",
)
def create_assignments(
    sessions_file: pathlib.Path,
    reviewers_file: pathlib.Path,
    regen: bool,
    verbose: bool,
) -> None:
    if ASSIGNMENTS_FILE.exists() and not regen:
        print(
            "Proposal assignments have been generated already. 🎉 "
            "Pass `--regen` if you want to regenerate them."
        )
        return

    sessions = get_sessions(sessions_file)
    reviewers = get_reviewers(reviewers_file)
    assignments = assign_reviewers(sessions, reviewers)
    write_assignments(assignments)
    if verbose:
        dump_stats(assignments)


@assignments.command("filter", help="Filter assignments by proposal or reviewer")
@click.option(
    "--proposal",
    "proposals",
    multiple=True,
    help="List of proposal IDs to filter assignments for",
)
@click.option(
    "--reviewer",
    "reviewers",
    multiple=True,
    help="List of rewviewer emails to filter assignments for",
)
@click.option(
    "--pretalx",
    is_flag=True,
    help="Print objects that can be uploaded to Pretalx to add assignments",
)
def filter_assignments(
    proposals: list[str],
    reviewers: list[str],
    pretalx: bool,
) -> None:
    if proposals and reviewers:
        print("Cannot filter with both `--proposal` and `--reviewer`. Please use only one.")
        raise click.Abort()

    if not proposals and not reviewers:
        print("Please provide at least one `--proposal` or `--reviewer` to filter with.")
        raise click.Abort()

    if not ASSIGNMENTS_FILE.exists():
        print(
            "Assignments have not been created yet. "
            "Use `cfp assignments create` to create them before filtering."
        )
        raise click.Abort()

    assignments = get_assignments(ASSIGNMENTS_FILE)
    if proposals:
        filter_assignments_by_proposal(assignments, proposals, pretalx=pretalx)
    if reviewers:
        filter_assignments_by_reviewer(assignments, reviewers, pretalx=pretalx)
