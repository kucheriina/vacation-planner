from models import VacationSchedule


def validate_vacation_schedule(
        new_schedule: VacationSchedule,
        actual_schedule: list[VacationSchedule]
):
    # 1. Дата начала отпуска раньше конца
    for period in new_schedule.periods:
        if period.start >= period.end:
            raise ValueError('Дата начала отпуска раньше конца')

    # * 2. Нельзя взять отпуск, который пересекается с другим разработчиком

    # 3. В каждом периоде должно быть не менее 2 выходных
    for period in new_schedule.periods:
        weekend_count = 0
        for i in range((period.end - period.start).days + 1):
            pass

    # 4. Общее число дней не должно быть меньше 28
    total_days_of_vacation = sum((p.end - p.start).days + 1 for p in new_schedule.periods)
    if total_days_of_vacation < 28:
        raise ValueError('Общее число дней не должно быть меньше 28')

    # 5. Сами периоды не должны пересекаться друг с другом
    periods = sorted(new_schedule.periods, key=lambda p: p.start)
    for i in range(len(periods) - 1):
        if periods[i].end >= periods[i + 1].start:
            raise ValueError(f'Периоды {periods[i]} и  {periods[i + 1]} пересекаются')

    # 6. Должен быть период 14 дней в графике
    two_weeks_period = any((p.end - p.start).days + 1 == 14 for p in new_schedule.periods)
    if not two_weeks_period:
        raise ValueError('Нет ни одного периода длиной 14 дней')

    return True
