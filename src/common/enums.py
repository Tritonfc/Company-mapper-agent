from enum import Enum


class ProgressStage(Enum):
    """Progress stages for the company mapper workflow."""

    VERIFYING = "verifying"
    VERIFIED = "verified"
    FINDING_PEOPLE = "finding_people"
    FOUND_PEOPLE = "found_people"
