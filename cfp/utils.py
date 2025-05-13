import csv
import dataclasses
import json
import pathlib
from typing import Mapping, Self


@dataclasses.dataclass
class Reviewer:
    name: str
    email: str

    @classmethod
    def from_row(cls, row: dict[str, str]) -> Self:
        return cls(name=row["Name"], email=row["Email"])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Reviewer):
            return NotImplemented
        return self.email == other.email

    def __hash__(self) -> int:
        return hash(self.email)


@dataclasses.dataclass
class Session:
    id: str
    title: str

    @classmethod
    def from_row(cls, row: dict[str, str]) -> Self:
        return cls(id=row["ID"], title=row["Proposal title"])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Session):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


@dataclasses.dataclass
class Assignment:
    session: Session
    reviewers: list[Reviewer]

    @classmethod
    def from_row(cls, id: str, row: dict[str, str]) -> Self:
        session = Session(id=id, title=row["title"])
        reviewers = [
            Reviewer(name=reviewer["name"], email=reviewer["email"])
            for reviewer in row["reviewers"]
        ]
        return cls(session=session, reviewers=reviewers)


def get_sessions(sessions_file: pathlib.Path) -> list[Session]:
    with open(sessions_file) as f:
        reader = csv.DictReader(f)
        return [Session.from_row(row) for row in reader]


def get_reviewers(reviewers_file: pathlib.Path) -> list[Reviewer]:
    with open(reviewers_file) as f:
        reader = csv.DictReader(f)
        return [Reviewer.from_row(row) for row in reader]


def get_assignments(assignments_file: pathlib.Path) -> list[Assignment]:
    with open(assignments_file) as f:
        j = json.load(f)
        return [
            Assignment.from_row(id=session_id, row=session_data)
            for session_id, session_data in j.items()
        ]


def write_assignments(assignments: Mapping[Session, list[Reviewer]]) -> None:
    with open("assignments.json", "w") as f:
        json.dump(
            {
                session.id: {
                    "title": session.title,
                    "reviewers": [
                        {"name": reviewer.name, "email": reviewer.email} for reviewer in reviewers
                    ],
                }
                for session, reviewers in assignments.items()
            },
            f,
            indent=4,
        )
