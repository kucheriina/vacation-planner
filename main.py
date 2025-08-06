from datetime import date
from models import VacationSchedule, VacationPeriod
from validations import validate_vacation_schedule


if __name__ == '__main__':
    existing_schedules = [
        VacationSchedule(
            employee_name='Emp1',
            periods=[
                VacationPeriod(date(2025, 2, 1), date(2025, 2, 10))
            ]
        ),
        VacationSchedule(
            employee_name='Emp2',
            periods=[
                VacationPeriod(date(2025, 3, 5), date(2025, 3, 20))
            ]
        )
    ]

    emp3_schedule = VacationSchedule(
        employee_name='Emp3',
        periods=[
            VacationPeriod(date(2025, 1, 8), date(2025, 1, 18)),
            VacationPeriod(date(2025, 2, 6), date(2025, 2, 15)),
            VacationPeriod(date(2025, 4, 1), date(2025, 4, 5))
        ]
    )

    try:
        validate_vacation_schedule(emp3_schedule, existing_schedules)
        print('График валиден')
    except ValueError as e:
        print(f'Ошибка валидации:\n{e}')
