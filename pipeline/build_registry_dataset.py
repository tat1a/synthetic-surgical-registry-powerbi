"""Build deterministic synthetic registry summary tables for the dashboard.

The script creates simulated surgical registry records and exports processed
summary tables at the same grain used by the Power BI report.
"""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from random import Random


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "data" / "processed"
SEED = 2402


COHORTS = {
    "breast": "Breast reconstruction",
    "nerve": "Peripheral nerve",
    "wound": "Complex wound",
}

TARGET_COMPLETIONS = {
    "breast": {30: 83, 90: 88, 180: 90, 365: 80},
    "nerve": {30: 84, 90: 90, 180: 94, 365: 71},
    "wound": {30: 92, 90: 85, 180: 83, 365: 72},
}

EVENT_COUNTS = {
    "breast": {"events": 14, "serious": 2},
    "nerve": {"events": 20, "serious": 2},
    "wound": {"events": 18, "serious": 1},
}

QUERY_COUNTS = {
    "CHRONOLOGY": 3,
    "COHORT_MISMATCH": 3,
    "FOLLOWUP_DUE": 15,
    "FOLLOWUP_STATUS": 3,
    "MODULE_MISSING": 3,
    "SAE_NOTIFICATION": 3,
}


@dataclass(frozen=True)
class Participant:
    participant_id: str
    cohort: str
    age_band: str
    enrolled_on: date


@dataclass(frozen=True)
class Procedure:
    procedure_id: str
    participant_id: str
    cohort: str
    procedure_on: date
    procedure_type: str


@dataclass(frozen=True)
class Followup:
    followup_id: str
    participant_id: str
    cohort: str
    day_target: int
    due_on: date
    status: str
    visit_on: date | None
    function_score: int | None


@dataclass(frozen=True)
class AdverseEvent:
    event_id: str
    procedure_id: str
    cohort: str
    event_on: date
    term: str
    severity: str
    serious: bool
    notified_on: date | None


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def build_participants() -> list[Participant]:
    rng = Random(SEED)
    age_bands = ["18-39", "40-59", "60-74", "75+"]
    start = date(2025, 1, 1)
    participants: list[Participant] = []

    for cohort in COHORTS:
        for index in range(1, 101):
            participant_id = f"{cohort[:2].upper()}-{index:03d}"
            participants.append(
                Participant(
                    participant_id=participant_id,
                    cohort=cohort,
                    age_band=rng.choice(age_bands),
                    enrolled_on=start + timedelta(days=rng.randrange(0, 180)),
                )
            )

    return participants


def build_procedures(participants: list[Participant]) -> list[Procedure]:
    procedure_names = {
        "breast": "reconstruction",
        "nerve": "nerve repair",
        "wound": "soft tissue coverage",
    }
    procedures = []

    for participant in participants:
        procedures.append(
            Procedure(
                procedure_id=f"PR-{participant.participant_id}",
                participant_id=participant.participant_id,
                cohort=participant.cohort,
                procedure_on=participant.enrolled_on + timedelta(days=7),
                procedure_type=procedure_names[participant.cohort],
            )
        )

    return procedures


def build_followups(participants: list[Participant]) -> list[Followup]:
    rng = Random(SEED + 1)
    followups: list[Followup] = []
    grouped: dict[str, list[Participant]] = defaultdict(list)

    for participant in participants:
        grouped[participant.cohort].append(participant)

    for cohort, cohort_participants in grouped.items():
        for day_target, completed_target in TARGET_COMPLETIONS[cohort].items():
            completed_ids = {
                p.participant_id
                for p in rng.sample(cohort_participants, completed_target)
            }
            for participant in cohort_participants:
                due_on = participant.enrolled_on + timedelta(days=day_target)
                completed = participant.participant_id in completed_ids
                followups.append(
                    Followup(
                        followup_id=f"FU-{participant.participant_id}-{day_target}",
                        participant_id=participant.participant_id,
                        cohort=cohort,
                        day_target=day_target,
                        due_on=due_on,
                        status="completed" if completed else "missed",
                        visit_on=due_on + timedelta(days=rng.randrange(-7, 8))
                        if completed
                        else None,
                        function_score=rng.randrange(35, 100) if completed else None,
                    )
                )

    return followups


def build_events(procedures: list[Procedure]) -> list[AdverseEvent]:
    rng = Random(SEED + 2)
    terms = ["infection", "bleeding", "readmission", "delayed healing"]
    events: list[AdverseEvent] = []
    procedures_by_cohort: dict[str, list[Procedure]] = defaultdict(list)

    for procedure in procedures:
        procedures_by_cohort[procedure.cohort].append(procedure)

    for cohort, counts in EVENT_COUNTS.items():
        selected = rng.sample(procedures_by_cohort[cohort], counts["events"])
        serious_ids = {procedure.procedure_id for procedure in selected[: counts["serious"]]}
        for idx, procedure in enumerate(selected, start=1):
            serious = procedure.procedure_id in serious_ids
            event_on = procedure.procedure_on + timedelta(days=rng.randrange(1, 45))
            events.append(
                AdverseEvent(
                    event_id=f"AE-{cohort[:2].upper()}-{idx:03d}",
                    procedure_id=procedure.procedure_id,
                    cohort=cohort,
                    event_on=event_on,
                    term=rng.choice(terms),
                    severity="serious" if serious else rng.choice(["mild", "moderate"]),
                    serious=serious,
                    notified_on=event_on + timedelta(days=1) if serious else None,
                )
            )

    return events


def cohort_counts(participants: list[Participant]) -> list[dict[str, object]]:
    counts = Counter(p.cohort for p in participants)
    return [
        {"cohort": cohort, "participant_count": counts[cohort]}
        for cohort in COHORTS
    ]


def followup_by_cohort(followups: list[Followup]) -> list[dict[str, object]]:
    rows = []
    for cohort in COHORTS:
        for day_target in [30, 90, 180, 365]:
            cohort_day = [
                f for f in followups
                if f.cohort == cohort and f.day_target == day_target
            ]
            completed = sum(1 for f in cohort_day if f.status == "completed")
            rows.append(
                {
                    "cohort": cohort,
                    "day_target": day_target,
                    "planned": len(cohort_day),
                    "completed": completed,
                    "missed": len(cohort_day) - completed,
                }
            )
    return rows


def ae_by_cohort(events: list[AdverseEvent]) -> list[dict[str, object]]:
    rows = []
    for cohort in COHORTS:
        cohort_events = [event for event in events if event.cohort == cohort]
        serious = [event for event in cohort_events if event.serious]
        rows.append(
            {
                "cohort": cohort,
                "event_count": len(cohort_events),
                "serious_count": len(serious),
                "unnotified_serious_count": sum(
                    1 for event in serious if event.notified_on is None
                ),
            }
        )
    return rows


def challenge_queries_by_rule() -> list[dict[str, object]]:
    return [
        {"rule_id": rule_id, "query_count": query_count}
        for rule_id, query_count in QUERY_COUNTS.items()
    ]


def field_completeness(
    participants: list[Participant],
    procedures: list[Procedure],
    followups: list[Followup],
    events: list[AdverseEvent],
) -> list[dict[str, object]]:
    return [
        {"table_name": "participants", "field_name": "participant_id", "nonmissing": len(participants), "rows": len(participants), "missing": 0},
        {"table_name": "participants", "field_name": "cohort", "nonmissing": len(participants), "rows": len(participants), "missing": 0},
        {"table_name": "participants", "field_name": "age_band", "nonmissing": len(participants), "rows": len(participants), "missing": 0},
        {"table_name": "participants", "field_name": "enrolled_on", "nonmissing": len(participants), "rows": len(participants), "missing": 0},
        {"table_name": "procedures", "field_name": "procedure_id", "nonmissing": len(procedures), "rows": len(procedures), "missing": 0},
        {"table_name": "procedures", "field_name": "participant_id", "nonmissing": len(procedures), "rows": len(procedures), "missing": 0},
        {"table_name": "procedures", "field_name": "cohort", "nonmissing": len(procedures), "rows": len(procedures), "missing": 0},
        {"table_name": "procedures", "field_name": "procedure_on", "nonmissing": len(procedures), "rows": len(procedures), "missing": 0},
        {"table_name": "procedures", "field_name": "procedure_type", "nonmissing": len(procedures), "rows": len(procedures), "missing": 0},
        {"table_name": "breast_module", "field_name": "procedure_id", "nonmissing": 100, "rows": 100, "missing": 0},
        {"table_name": "breast_module", "field_name": "intent", "nonmissing": 100, "rows": 100, "missing": 0},
        {"table_name": "breast_module", "field_name": "laterality", "nonmissing": 100, "rows": 100, "missing": 0},
        {"table_name": "breast_module", "field_name": "implant_used", "nonmissing": 100, "rows": 100, "missing": 0},
        {"table_name": "nerve_module", "field_name": "procedure_id", "nonmissing": 100, "rows": 100, "missing": 0},
        {"table_name": "nerve_module", "field_name": "injury_level", "nonmissing": 100, "rows": 100, "missing": 0},
        {"table_name": "nerve_module", "field_name": "technique", "nonmissing": 100, "rows": 100, "missing": 0},
        {"table_name": "nerve_module", "field_name": "target_function", "nonmissing": 100, "rows": 100, "missing": 0},
        {"table_name": "wound_module", "field_name": "procedure_id", "nonmissing": 100, "rows": 100, "missing": 0},
        {"table_name": "wound_module", "field_name": "region", "nonmissing": 100, "rows": 100, "missing": 0},
        {"table_name": "wound_module", "field_name": "coverage", "nonmissing": 100, "rows": 100, "missing": 0},
        {"table_name": "wound_module", "field_name": "defect_size", "nonmissing": 100, "rows": 100, "missing": 0},
        {"table_name": "followups", "field_name": "followup_id", "nonmissing": len(followups), "rows": len(followups), "missing": 0},
        {"table_name": "followups", "field_name": "participant_id", "nonmissing": len(followups), "rows": len(followups), "missing": 0},
        {"table_name": "followups", "field_name": "day_target", "nonmissing": len(followups), "rows": len(followups), "missing": 0},
        {"table_name": "followups", "field_name": "due_on", "nonmissing": len(followups), "rows": len(followups), "missing": 0},
        {"table_name": "followups", "field_name": "status", "nonmissing": len(followups), "rows": len(followups), "missing": 0},
        {"table_name": "followups", "field_name": "visit_on", "nonmissing": sum(1 for f in followups if f.visit_on is not None), "rows": len(followups), "missing": sum(1 for f in followups if f.visit_on is None)},
        {"table_name": "followups", "field_name": "function_score", "nonmissing": sum(1 for f in followups if f.function_score is not None), "rows": len(followups), "missing": sum(1 for f in followups if f.function_score is None)},
        {"table_name": "adverse_events", "field_name": "event_id", "nonmissing": len(events), "rows": len(events), "missing": 0},
        {"table_name": "adverse_events", "field_name": "procedure_id", "nonmissing": len(events), "rows": len(events), "missing": 0},
        {"table_name": "adverse_events", "field_name": "event_on", "nonmissing": len(events), "rows": len(events), "missing": 0},
        {"table_name": "adverse_events", "field_name": "term", "nonmissing": len(events), "rows": len(events), "missing": 0},
        {"table_name": "adverse_events", "field_name": "severity", "nonmissing": len(events), "rows": len(events), "missing": 0},
        {"table_name": "adverse_events", "field_name": "serious", "nonmissing": len(events), "rows": len(events), "missing": 0},
        {"table_name": "adverse_events", "field_name": "notified_on", "nonmissing": sum(1 for e in events if e.notified_on is not None), "rows": len(events), "missing": sum(1 for e in events if e.notified_on is None)},
    ]


def main() -> None:
    participants = build_participants()
    procedures = build_procedures(participants)
    followups = build_followups(participants)
    events = build_events(procedures)

    write_csv(
        OUTPUT_DIR / "cohort_counts.csv",
        cohort_counts(participants),
        ["cohort", "participant_count"],
    )
    write_csv(
        OUTPUT_DIR / "followup_by_cohort.csv",
        followup_by_cohort(followups),
        ["cohort", "day_target", "planned", "completed", "missed"],
    )
    write_csv(
        OUTPUT_DIR / "ae_by_cohort.csv",
        ae_by_cohort(events),
        ["cohort", "event_count", "serious_count", "unnotified_serious_count"],
    )
    write_csv(
        OUTPUT_DIR / "challenge_queries_by_rule.csv",
        challenge_queries_by_rule(),
        ["rule_id", "query_count"],
    )
    write_csv(
        OUTPUT_DIR / "field_completeness.csv",
        field_completeness(participants, procedures, followups, events),
        ["table_name", "field_name", "nonmissing", "rows", "missing"],
    )


if __name__ == "__main__":
    main()
