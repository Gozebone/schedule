import datetime
import math
from parse.parser import Lesson


def create_calendar(service, calendar_name):
    calendar = {"summary": calendar_name, "timeZone": "Europe/Moscow"}

    service.calendars().insert(body=calendar).execute()


def is_schedule_calendar_exists(service, calendar_name):
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list["items"]:
            if calendar_list_entry["summary"] == calendar_name:
                return True

        page_token = calendar_list.get("nextPageToken")
        if not page_token:
            break

    return False


def get_schedule_calendar(service, calendar_name):
    page_token = None
    schedule_calendar = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list["items"]:
            if calendar_list_entry["summary"] == calendar_name:
                schedule_calendar = calendar_list_entry
                break

        page_token = calendar_list.get("nextPageToken")
        if not page_token:
            break
    if schedule_calendar == None:
        print(f"No {calendar_name} calendar found\nCheck if you have renamed it")

    return schedule_calendar


def create_event(service, calendar, event):
    event = service.events().insert(calendarId=calendar["id"], body=event).execute()
    # print(
    #     "Event created in calendar: %s \nLink: %s"
    #     % (calendar["summary"], event.get("htmlLink"))
    # )


def delete_event(service, calendar, id):
    service.events().delete(calendarId=calendar["id"], eventId=id).execute()


def get_events(service, calendar, amount: int):
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    events_result = (
        service.events()
        .list(
            calendarId=calendar["id"],
            timeMin=now,
            maxResults=amount,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    return events_result.get("items", [])


def get_events_by_time(service, calendar, start, end):
    events_result = (
        service.events()
        .list(
            calendarId=calendar["id"],
            timeMin=start,
            timeMax=end,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    return events_result.get("items", [])


def get_events_by_date(service, calendar, cur_date: str) -> list[dict]:
    start = to_iso_time_format(cur_date, "00:00")
    end = to_iso_time_format(cur_date, "23:59")
    return get_events_by_time(service, calendar, start, end)


def event_exists(new_event, existing_events) -> bool:
    for event in existing_events:
        if new_event["start"]["dateTime"] == event["start"]["dateTime"]:
            if new_event["summary"] == event["summary"]:
                if new_event["description"] == event["description"]:
                    return True

    return False


def build_event(lesson: Lesson, cur_date: str) -> dict:
    event = {
        "summary": lesson.lesson,
        "location": lesson.address,
        "description": lesson.room,
        "start": {
            "dateTime": to_iso_time_format(cur_date, lesson.start_time),
        },
        "end": {
            "dateTime": to_iso_time_format(cur_date, lesson.end_time),
        },
        "colorId": get_color_by_type(lesson.type),
        "reminders": {
            "useDefault": False,
            # "overrides": [ {"method": "popup", "minutes": 10} ]
        },
    }

    return event


def get_color_by_type(id: int) -> int:
    if id == 0:
        return 1  # Lavender
    elif id == 1:
        return 5  # Banana
    elif id == 2:
        return 3  # Grape
    else:
        return 8


def to_iso_time_format(date: str, time: str) -> str:
    return date + "T" + time + ":00+03:00"
