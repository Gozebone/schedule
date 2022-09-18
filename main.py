from datetime import date, timedelta
import google_calendar.event_funcs as event_funcs
import google_calendar.google_service as google_service
import parse.parser as parser


def main():
    service = google_service.get_service()

    # getting google calendar
    if not event_funcs.is_schedule_calendar_exist(service):
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
    group = input("Enter group number in M3107 format: ").capitalize()
    week = parser.get_schedule(group)
    
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    
    #TODO update event if its already exist
    for day in week.days:
        cur_date = str(start_of_week + timedelta(days=day.day_index))
        for lesson in day.lessons:
            start = cur_date + 'T' + lesson.time_start + ':00+03:00'

            end = cur_date + 'T' + lesson.time_end + ':00+03:00'

            event = {
                'summary': lesson.lesson,
                'location': lesson.address,
                'description': lesson.room,
                'start': {
                    'dateTime': start,
                },
                'end': {
                    'dateTime': end,
                },
                'colorId': lesson.type + 1,  # colors goes from 1 to 12
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }
            event_funcs.create_event(service, schedule_calendar, event)
            
if __name__ == '__main__':
    main()
