import json
import random
from collections import defaultdict

from rich import print
from rich.table import Table

from cfp.utils import Assignment, Reviewer, Session

MAX_REVIEWS_PER_REVIEWER = 30
REVIEWERS_PER_PROPOSAL = 2

random.seed(5515459164160430685)


def assign_reviewers(sessions: list[Session], reviewers: list[Reviewer]) -> list[Assignment]:
    reviewers_load: defaultdict[Reviewer, int] = defaultdict(int)
    assignments: list[Assignment] = []
    random.shuffle(sessions)

    for session in sessions:
        available_reviewers: list[Reviewer] = [
            r for r in reviewers if reviewers_load[r] < MAX_REVIEWS_PER_REVIEWER
        ]

        assignment = Assignment(session=session, reviewers=[])
        while len(assignment.reviewers) < REVIEWERS_PER_PROPOSAL:
            r = random.choice(available_reviewers)
            if r not in assignment.reviewers:
                assignment.reviewers.append(r)
                reviewers_load[r] += 1
        assignments.append(assignment)

    return assignments


def dump_stats(assignments: list[Assignment]) -> None:
    print("Sessions per reviewer:")
    reviewer_load = defaultdict(int)
    for assignment in assignments:
        for reviewer in assignment.reviewers:
            reviewer_load[reviewer] += 1
    for reviewer, load in reviewer_load.items():
        print(f"\t{reviewer.name}: {load}")


def filter_assignments_by_proposal(
    assignments: list[Assignment], proposals: list[str], *, pretalx: bool = False
) -> None:
    proposal_to_reviewers: dict[Session, list[Reviewer]] = {
        assignment.session: assignment.reviewers
        for assignment in assignments
        if assignment.session.id in proposals
    }
    if pretalx:
        pretalx_obj = {
            session.id: [reviewer.email for reviewer in reviewers]
            for session, reviewers in proposal_to_reviewers.items()
        }
        print(json.dumps(pretalx_obj))
    else:
        for session, reviewers in proposal_to_reviewers.items():
            table = Table(title=f"Reviewers for {session.title!r}")
            table.add_column("Name")
            table.add_column("Email")

            for reviewer in reviewers:
                table.add_row(reviewer.name, reviewer.email)

            print(table)


def filter_assignments_by_reviewer(
    assignments: list[Assignment], reviewers: list[str], *, pretalx
) -> None:
    reviewer_to_proposals: defaultdict[Reviewer, list[Session]] = defaultdict(list)
    for assignment in assignments:
        for reviewer in assignment.reviewers:
            if reviewer.email in reviewers:
                reviewer_to_proposals[reviewer].append(assignment.session)
    if pretalx:
        pretalx_obj = {
            reviewer.email: [session.id for session in sessions]
            for reviewer, sessions in reviewer_to_proposals.items()
        }
        print(json.dumps(pretalx_obj))
    else:
        for reviewer, sessions in reviewer_to_proposals.items():
            table = Table(title=f"Assigned proposals for {reviewer.name} ({reviewer.email})")
            table.add_column("ID")
            table.add_column("Title")

            for session in sessions:
                table.add_row(session.id, session.title)

            print(table)
