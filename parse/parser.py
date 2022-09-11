import requests
from bs4 import BeautifulSoup
from selenium import webdriver


class Lesson:
    def __init__(self, tr):
        self.time_start, self.time_end = self.time_parse(
            tr.select(".time > span")[0].get_text())
        self.room = self.room_parse(tr.select(".room > dl > dd")[0].get_text())
        self.address = self.address_parse(
            tr.select(".room > dl > dt > span")[0].get_text())
        self.lesson, self.type = self.lesson_parse(
            tr.select(".lesson > dl > dd")[0].get_text())

    @staticmethod
    def time_parse(time):
        return time[:5], time[6:]

    @staticmethod
    def room_parse(room):
        return room[:4]

    @staticmethod
    def address_parse(address):
        return address
        # return address[:address.find(' ')]

    @staticmethod
    def lesson_parse(lesson):
        open_br_index = lesson.find('(')
        close_br_index = lesson.find(')')
        lesson_type = lesson[open_br_index + 1:close_br_index]
        lesson_type_index = -1

        if lesson_type.upper() == 'ЛЕК':
            lesson_type_index = 0
        elif lesson_type.upper() == 'ПРАК':
            lesson_type_index = 1
        elif lesson_type.upper() == 'ЛАБ':
            lesson_type_index = 2

        return lesson[:open_br_index], lesson_type_index


class Day:
    def __init__(self, day_schedule_html, day_index):
        self.lessons = []
        self.day_index = day_index
        tr_array = day_schedule_html.select('tr')
        for current_lesson in tr_array:
            self.lessons.append(Lesson(current_lesson))


class Week:
    def __init__(self, schedule_html):
        self.days = []
        for index, current_day in enumerate(schedule_html):
            if current_day is not None:
                self.days.append(Day(current_day, index))


def group_number_generator(group):
    return f'https://itmo.ru/ru/schedule/0/{group}/1/raspisanie_zanyatiy_{group}.htm'


def schedule_by_group(group):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

    group_url = group_number_generator(group)

    req = requests.get(group_url)

    string = req.text.replace('<tbody><th', '<tbody><tr><th')
    string_2 = string.replace('<tr></tbody>', '</tbody>')

    soup = BeautifulSoup(bytes(string_2, 'utf-8'), 'lxml')

    # driver = webdriver.Chrome()

    # driver.get(group_url)

    # html = driver.page_source

    # soup = BeautifulSoup(html)

    # f = open("response.txt", "w")
    # f.write(req.content.__str__())
    # f.close()

    schedule_html = []
    for day in range(1, 7):
        schedule_html.append(soup.find(id=f'{day}day'))

    return schedule_html


def get_schedule(group):
    return Week(schedule_by_group(group))
