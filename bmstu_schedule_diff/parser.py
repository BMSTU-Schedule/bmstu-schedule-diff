# bmstu-schedule-diff
# Copyright (C) 2018 BMSTU Schedule (George Gabolaev)
# Copyright (C) 2019 Nikola Trubitsyn

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
from typing import List

import bmstu_schedule
import requests
from bmstu_schedule import Lesson
from bs4 import BeautifulSoup


# from bmstu_schedule
def get_api_date():
    r = requests.get(url=bmstu_schedule.configs.API_URL)
    return r.json()['semester_start_date']


# from bmstu_schedule
def date_parser(date):
    return datetime.strptime(date, bmstu_schedule.configs.DATE_FORMAT)


# from bmstu_schedule
def get_schedule(group_code: str) -> List[Lesson]:
    semester_first_monday = date_parser(get_api_date())
    bmstu_schedule.Subject.semester_start_date = semester_first_monday

    list_page_response = requests.get(bmstu_schedule.configs.MAIN_URL + bmstu_schedule.configs.GROUPS_LIST_URL)
    soup = BeautifulSoup(list_page_response.content, 'lxml')
    lessons = []
    outdir = "./"

    for valid_group_code, url in bmstu_schedule.get_urls(group_code, outdir, soup):
        page_html = requests.get(url)
        soup = BeautifulSoup(page_html.content, 'lxml')

        for dID, day in enumerate(soup.select('div.col-md-6.hidden-xs')):
            day_table = day.contents[1]
            rows = day_table.findAll('tr')
            for row in rows[2:]:
                lesson = parse_row(row.contents, dID)
                if lesson:
                    lessons.append(lesson)
    return lessons


# from bmstu_schedule
def parse_row(cells, day_number) -> Lesson:
    if len(set(cell for cell in cells[3:5])) > 1:
        subjects = []
        timing = cells[1].string

        for c in range(3, 5):
            try:
                subjects.append(
                    bmstu_schedule.Subject(
                        (cells[c].contents[i].string for i in range(0, 7, 2)),
                        day_number,
                        weeks_interval=(
                            2 if cells[3].attrs != {
                                'colspan': '2'
                            } else 1
                        ),
                        denominator=(c == 4)
                    )
                )
            except (IndexError, AttributeError):
                pass

        return Lesson(timing, subjects)
