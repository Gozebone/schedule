from datetime import date, timedelta
import sys
import re

import calendar_logic.google_calendar.event_funcs as event_funcs
import calendar_logic.google_calendar.google_service as google_service
import calendar_logic.parse.parser as parser


def add_events(group: str):
    service = google_service.get_service()
    
    # getting google calendar
    if not event_funcs.is_schedule_calendar_exists(service):
        print(f"You dont have a {event_funcs.CALENDAR_NAME} calendar, create it? (Y/N): ")
        while True:
            answer = input()
            if answer == "Y":
                print("Creating calendar")
                event_funcs.create_calendar(service)
                break
            elif answer == "N":
                print("Terminating...")
                return
            else:
                #TODO ask if user wants to use some other calendar
                print("Unexpected answer, try again (Y/N): ")
                continue         
    
    schedule_calendar = event_funcs.get_schedule_calendar(service)
    
    # schedule parse
    # while True:
    #     group = input("Enter group number in M3136 format: ").capitalize()
    #     if (re.match(r'\b[A-Z]\d[1-5]\d{2}\b', group)):
    #         break
    #     else:
    #         print("Wrong input")
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    
    week = parser.get_schedule(group, today.isocalendar().week % 2)
    
    if sys.argv.count("-n") > 0:
        start_of_week += timedelta(weeks=1)
        
    for day in week.days:
        cur_date = str(start_of_week + timedelta(days=day.day_index))
        existing_events = event_funcs.get_events_by_date(service, schedule_calendar, cur_date)
        for lesson in day.lessons:
            if (re.match(r'\d{2}:\d{2}', lesson.time_start) == None):
                continue
            event = event_funcs.build_event(lesson, cur_date)
            if (not event_funcs.event_exists(event, existing_events)):
                event_funcs.create_event(service, schedule_calendar, event)
                pass
