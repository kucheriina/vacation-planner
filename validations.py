from models import VacationSchedule
from datetime import timedelta
import calendar


def validate_vacation_schedule(
        new_schedule: VacationSchedule,
        actual_schedule: list[VacationSchedule]
):
    # 1. Дата начала отпуска раньше конца
    for period in new_schedule.periods:
        if period.start >= period.end:
            raise ValueError('Дата начала отпуска раньше конца')

    # 2. Нельзя взять отпуск, который пересекается с другим разработчиком
    for other_schedule in actual_schedule:
        if other_schedule.employee_name == new_schedule.employee_name:
            continue  # пропускаем самого себя
        for other_period in other_schedule.periods:
            for period in new_schedule.periods:
                if period.start < other_period.end and other_period.start < period.end:
                    raise ValueError(
                        f'Отпуск {period} пересекается с отпуском {other_schedule.employee_name} ({other_period})'
                    )

    # 3. В каждом периоде должно быть не менее 2 выходных
    for period in new_schedule.periods:
        weekend_count = 0
        current_day = period.start
        while current_day <= period.end:
            if calendar.weekday(current_day.year, current_day.month, current_day.day) in (5, 6):  # Сб, Вс
                weekend_count += 1
            current_day += timedelta(days=1)
        if weekend_count < 2:
            raise ValueError(f'Период {period} содержит меньше двух выходных ({weekend_count})')

    # 4. Общее число дней не должно быть меньше 28
    total_days_of_vacation = sum((p.end - p.start).days + 1 for p in new_schedule.periods)
    if total_days_of_vacation < 28:
        raise ValueError('Общее число дней не должно быть меньше 28')

    # 5. Сами периоды не должны пересекаться друг с другом
    periods = sorted(new_schedule.periods, key=lambda p: p.start)
    for i in range(len(periods) - 1):
        if periods[i].end >= periods[i + 1].start:
            raise ValueError(f'Периоды {periods[i]} и {periods[i + 1]} пересекаются')

    # 6. Должен быть период 14 дней в графике
    two_weeks_period = any((p.end - p.start).days + 1 == 14 for p in new_schedule.periods)
    if not two_weeks_period:
        raise ValueError('Нет ни одного периода длиной 14 дней')

    return True