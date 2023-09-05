import requests
from bs4 import BeautifulSoup


class Lesson:
    def __init__(self, lesson, start_time, end_time, room, address, type, weeks=2):
        self.lesson = lesson
        self.start_time = start_time
        self.end_time = end_time
        self.room = room
        self.address = address
        self.type = type
        self.weeks = weeks  # 0 - even, 1 - odd, 2 - all time

    @classmethod
    def from_html(cls, tr):
        start_time, end_time = cls.time_parse(tr.select(".time > span")[0].get_text())
        room = cls.room_parse(tr.select(".room > dl > dd")[0].get_text())
        address = cls.address_parse(tr.select(".room > dl > dt > span")[0].get_text())
        lesson, type = cls.lesson_parse(tr.select(".lesson > dl > dd")[0].get_text())
        return cls(lesson, start_time, end_time, room, address, type)

    def serialize(self) -> dict:
        return {
            "lesson": self.lesson,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "room": self.room,
            "address": self.address,
            "type": self.type,
            "weeks": self.weeks,
        }

    @classmethod
    def deserialize(cls, obj):
        return cls(
            obj["lesson"],
            obj["start_time"],
            obj["end_time"],
            obj["room"],
            obj["address"],
            obj["type"],
            obj["weeks"] if "weeks" in obj else 2,
        )

    @staticmethod
    def time_parse(time: str) -> tuple[str, str]:
        return time[:5], time[6:]

    @staticmethod
    def room_parse(room: str) -> str:
        return room[:4]

    @staticmethod
    def address_parse(address: str) -> str:
        return address

    @staticmethod
    def lesson_parse(lesson: str) -> tuple[str, int]:
        open_br_index = lesson.find("(")
        close_br_index = lesson.find(")")
        lesson_type = lesson[open_br_index + 1 : close_br_index]
        lesson_type_index = -1

        if lesson_type.upper() == "ЛЕК":
            lesson_type_index = 0
        elif lesson_type.upper() == "ПРАК":
            lesson_type_index = 1
        elif lesson_type.upper() == "ЛАБ":
            lesson_type_index = 2

        return lesson[:open_br_index], lesson_type_index


class Day:
    def __init__(self, lessons, day_index):
        self.lessons = lessons
        self.day_index = day_index

    @classmethod
    def from_html(cls, day_schedule_html, day_index):
        return cls(
            [Lesson.from_html(lesson) for lesson in day_schedule_html.select("tr")],
            day_index,
        )

    def serialize(self) -> dict:
        return {
            "day_index": self.day_index,
            "lessons": [lesson.serialize() for lesson in self.lessons],
        }

    @classmethod
    def deserialize(cls, obj: dict):
        return cls(
            [Lesson.deserialize(lesson) for lesson in obj["lessons"]], obj["day_index"]
        )


class Week:
    def __init__(self, days):
        self.days = days

    @classmethod
    def from_html(cls, schedule_html):
        return cls(
            [
                Day.from_html(current_day, index)
                for index, current_day in enumerate(
                    filter(lambda current_day: current_day is not None, schedule_html)
                )
            ]
        )

    def serialize(self) -> dict:
        return {"week": [day.serialize() for day in self.days]}

    @classmethod
    def deserialize(cls, obj: dict):
        return cls([Day.deserialize(day) for day in obj["week"]])


def group_number_generator(group: str) -> str:
    return f"https://itmo.ru/ru/schedule/0/{group}/1/raspisanie_zanyatiy_{group}.htm"


def schedule_by_group(group: str) -> list[str]:
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "3600",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    }

    group_url = group_number_generator(group)

    req = requests.get(group_url, headers)

    string = req.text.replace("<tbody><th", "<tbody><tr><th")
    string_2 = string.replace("<tr></tbody>", "</tbody>")

    soup = BeautifulSoup(bytes(string_2, "utf-8"), "html.parser")

    schedule_html = []
    for day in range(1, 7):
        schedule_html.append(soup.find(id=f"{day}day"))

    return schedule_html


def get_schedule(group: str) -> Week:
    return Week.from_html(schedule_by_group(group))
