from datetime import date
from models import VacationSchedule, VacationPeriod
from validations import validate_vacation_schedule

if __name__ == '__main__':
    existing_schedules = [
        VacationSchedule(
            employee_name='Emp1',
            periods=[VacationPeriod(date(2025, 2, 1), date(2025, 2, 10))]
        ),
        VacationSchedule(
            employee_name='Emp2',
            periods=[VacationPeriod(date(2025, 3, 5), date(2025, 3, 20))]
        )
    ]

    # --- 1. Дата начала >= конца
    try:
        validate_vacation_schedule(
            VacationSchedule('Test', [VacationPeriod(date(2025, 5, 10), date(2025, 5, 5))]),
            existing_schedules
        )
        assert False, "Ожидалась ошибка для начала >= конца"
    except ValueError as e:
        assert 'Дата начала отпуска раньше конца' in str(e)

    # --- 2. Пересечение с другим сотрудником
    try:
        validate_vacation_schedule(
            VacationSchedule('Test', [VacationPeriod(date(2025, 2, 5), date(2025, 2, 12))]),
            existing_schedules
        )
        assert False, "Ожидалась ошибка пересечения с другим сотрудником"
    except ValueError as e:
        assert 'пересекается с отпуском Emp1' in str(e), str(e)

    # --- 3. Меньше 2 выходных в периоде
    try:
        validate_vacation_schedule(
            VacationSchedule('Test', [VacationPeriod(date(2025, 5, 5), date(2025, 5, 6))]),  # Пн-Вт
            existing_schedules
        )
        assert False, "Ожидалась ошибка для менее чем 2 выходных"
    except ValueError as e:
        assert 'содержит меньше двух выходных' in str(e), str(e)

    # --- 4. Общее число дней < 28
    try:
        validate_vacation_schedule(
            VacationSchedule('Test', [VacationPeriod(date(2025, 5, 1), date(2025, 5, 10))]),
            existing_schedules
        )
        assert False, "Ожидалась ошибка для <28 дней"
    except ValueError as e:
        assert 'Общее число дней не должно быть меньше 28' in str(e), str(e)

    # --- 5. Пересечение периодов внутри одного графика (сумма дней >= 28)
    try:
        validate_vacation_schedule(
            VacationSchedule('Test', [
                VacationPeriod(date(2025, 5, 1), date(2025, 5, 15)),  # 15 дней
                VacationPeriod(date(2025, 5, 10), date(2025, 5, 24))  # 15 дней
            ]),
            existing_schedules
        )
        assert False, "Ожидалась ошибка пересечения внутри одного графика"
    except ValueError as e:
        assert 'Периоды' in str(e) and 'пересекаются' in str(e), str(e)

    # --- 6. Нет периода 14 дней (сумма дней >=28)
    try:
        validate_vacation_schedule(
            VacationSchedule('Test', [VacationPeriod(date(2025, 5, 1), date(2025, 5, 28))]),  # 28 дней
            existing_schedules
        )
        assert False, "Ожидалась ошибка отсутствия 14-дневного периода"
    except ValueError as e:
        assert 'Нет ни одного периода длиной 14 дней' in str(e), str(e)

    # --- Успешный тест
    assert validate_vacation_schedule(
        VacationSchedule('Emp3', [
            VacationPeriod(date(2025, 1, 8), date(2025, 1, 18)),  # 11 дней
            VacationPeriod(date(2025, 2, 20), date(2025, 3, 5)),  # 14 дней
            VacationPeriod(date(2025, 4, 1), date(2025, 4, 15))   # 15 дней
        ]),
        existing_schedules
    ) is True

    print("Все тесты прошли успешно")