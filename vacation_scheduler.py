from models import VacationSchedule, VacationPeriod
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import time


def run_vacation_scheduler(employees: list[str], tz_name: str):
    tz = ZoneInfo(tz_name)
    schedules: dict[str, VacationSchedule] = {}

    now = datetime.now(tz)
    create_time = now
    reminder_time = now + timedelta(minutes=1)
    close_time = now + timedelta(minutes=2)

    def create_empty_schedules():
        for employee in employees:
            schedules[employee] = VacationSchedule(employee_name=employee, periods=[])
        print(f"[{datetime.now(tz)}] Созданы пустые графики отпусков для всех сотрудников")

    def send_reminders():
        for employee in employees:
            print(f"[{datetime.now(tz)}] Отправлено уведомление сотруднику: {employee}")

    def close_schedules():
        for employee, schedule in schedules.items():
            if not schedule.periods:
                schedule.periods = [
                    VacationPeriod(start=datetime(now.year + 1, 9, 1).date(), end=datetime(now.year + 1, 9, 14).date()),
                    VacationPeriod(start=datetime(now.year + 1, 7, 1).date(), end=datetime(now.year + 1, 7, 14).date())
                ]
            print(f"График для сотрудника {employee} заполнен автоматически")
        print(f"[{datetime.now(tz)}] Приём графиков отпусков закрыт")

    print(f"[{now}] Воркер запущен. Часовой пояс: {tz_name}")

    done_create = False
    done_reminder = False
    done_close = False

    while True:
        now_time = datetime.now(tz)

        if not done_create and now_time >= create_time:
            create_empty_schedules()
            done_create = True

        if not done_reminder and now_time >= reminder_time:
            send_reminders()
            done_reminder = True

        if not done_close and now_time >= close_time:
            close_schedules()
            done_close = True

        if done_create and done_reminder and done_close:
            print("Все задачи выполнены")
            break

        time.sleep(1)


employees_test = ["Иван", "Мария", "Алексей", "Ольга"]
run_vacation_scheduler(employees_test, tz_name="Europe/Saratov")
