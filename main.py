from datetime import date, timedelta
import google_calendar.event_funcs as event_funcs
import google_calendar.google_service as google_service
import parse.parser as parser


def main():
    service = google_service.get_service()
    group = input().capitalize()

    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())

    week = parser.get_schedule(group)

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
            }
            event_funcs.create_event(service, event)
            
if __name__ == '__main__':
    main()
