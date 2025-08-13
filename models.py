from dataclasses import dataclass
from datetime import date


@dataclass
class VacationPeriod:
    start: date
    end: date


@dataclass
class VacationSchedule:
    employee_name: str
    periods: list[VacationPeriod]
