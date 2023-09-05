from datetime import date, timedelta
import sys
import google_calendar.event_funcs as event_funcs
import google_calendar.google_service as google_service
import parse.parser as parser
import re
import os
import json


def fetch_schedule(group) -> parser.Week:
    while True:
        group = input("Enter group number: ").capitalize() if group is None else group
        if re.match(r"\b[A-Z]\d[1-5]\d{2}\b", group):
            break
        else:
            group = None
            print("Invalid group number")

    return parser.get_schedule(group)


# TODO: make flag to pass calendar name and json path

# SCHEDULE_FILE_PATH = "schedule.json"
# CALENDAR_NAME = "ITMO Schedule"

SCHEDULE_FILE_PATH = "schedule-phy.json"
CALENDAR_NAME = "Polytech Schedule"


def load_schedule() -> parser.Week:
    with open(SCHEDULE_FILE_PATH, "r", encoding="utf8") as file:
        return parser.Week.deserialize(json.loads(file.read()))


def save_schedule(week: parser.Week):
    with open(SCHEDULE_FILE_PATH, "w", encoding="utf8") as file:
        json.dump(week.serialize(), file, ensure_ascii=False)


def get_calendar(service):
    if not event_funcs.is_schedule_calendar_exists(service, CALENDAR_NAME):
        print(f"You dont have a {CALENDAR_NAME} calendar, create it? (Y/N): ")
        while True:
            answer = input()
            if answer == "Y":
                print("Creating calendar")
                event_funcs.create_calendar(service, CALENDAR_NAME)
                break
            elif answer == "N":
                print("Terminating...")
                return
            else:
                print("Unexpected answer, try again (Y/N): ")
                continue

    return event_funcs.get_schedule_calendar(service, CALENDAR_NAME)


class Flags:
    FETCH = "fetch"
    CACHE = "cache"

    def __init__(self):
        self.scheule_source = self.CACHE
        self.group = None
        self.push = False
        self.save = False
        self.help = False
        self.remove = False
        self.next_week = False


def parse_flags(args: list) -> Flags:
    flags = Flags()

    if args.count("-h"):
        flags.help = True

    if args.count("-f"):
        flags.scheule_source = Flags.FETCH
        i = args.index("-f")
        if len(args) > i + 1:
            if args[i + 1][:1] != "-":
                flags.group = args[i + 1]
    else:
        flags.scheule_source = Flags.CACHE

    if args.count("-p"):
        flags.push = True

    if args.count("-s"):
        flags.save = True

    if args.count("-r"):
        flags.remove = True

    if args.count("-n"):
        flags.next_week = True

    return flags


def main():
    if len(sys.argv) <= 1:
        print("No flags.")
        print("Use -h for help")
        return

    flags = parse_flags(sys.argv)

    if flags.help:
        print("=== Google Calendar Schedule Tool ===")
        print()
        print("FLAGS:")
        print("  -h -- show this message")
        print("Schedule sources:")
        print("  -f [GROUP NUMBER] -- fetch schedule from itmo.ru")
        print(f"  -c -- use schedule from local '{SCHEDULE_FILE_PATH}' file")
        print("Actions: (by default -c is used)")
        print(f"  -s -- save schedule to '{SCHEDULE_FILE_PATH}'")
        print("  -p -- push schedule to Google Calendar")
        print("  -r -- remove schedule-related events from Google Calendar")

        return

    if flags.scheule_source == flags.FETCH:
        week = fetch_schedule(flags.group)
    else:
        if os.path.exists(SCHEDULE_FILE_PATH):
            week = load_schedule()
        else:
            print(
                f"'{SCHEDULE_FILE_PATH}' doesn't exist. Create it or run with -f flag to fetch schedule."
            )
            print("Use -h for help")
            return

    if flags.save:
        save_schedule(week)

    if flags.push or flags.remove:
        service = google_service.get_service()
        schedule_calendar = get_calendar(service)

        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        if flags.next_week:
            start_of_week += timedelta(weeks=1)

        if flags.remove:
            for day in week.days:
                cur_date = str(start_of_week + timedelta(days=day.day_index))
                existing_events = event_funcs.get_events_by_date(
                    service, schedule_calendar, cur_date
                )
                for event in existing_events:
                    event_funcs.delete_event(service, schedule_calendar, event["id"])
            print(f"=== Events removed ===")

        if flags.push:
            events_created = 0
            cur_week = (today.isocalendar().week + flags.next_week) % 2 + 1
            for day in week.days:
                cur_date = str(start_of_week + timedelta(days=day.day_index))
                existing_events = event_funcs.get_events_by_date(
                    service, schedule_calendar, cur_date
                )
                for lesson in day.lessons:
                    if (
                        re.match(r"\d?\d:\d{2}", lesson.start_time) is not None
                        and (lesson.weeks + 1) & cur_week
                    ):
                        event = event_funcs.build_event(lesson, cur_date)
                        if not event_funcs.event_exists(event, existing_events):
                            event_funcs.create_event(service, schedule_calendar, event)
                            events_created += 1

            print(f"=== {events_created} event(s) created ===")


if __name__ == "__main__":
    main()


# TODO:
#   add schedule merge (fetched and cached)
