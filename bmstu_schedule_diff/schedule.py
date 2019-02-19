# bmstu-schedule-diff
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

from typing import Dict, List, Tuple

from bmstu_schedule import Subject, Lesson

from .diff import Diff

WEEK_START = 0
WEEK_END = 5


class Schedule(object):

    def __init__(self, group: str, subjects_by_weekday: Dict[int, List[Subject]]):
        self.group = group
        self.subjects_by_weekday = subjects_by_weekday

    def diff(self, schedule, flags: int) -> Dict[int, List[Tuple[Subject, Subject]]]:
        weekdays = {}

        for weekday in range(WEEK_START, WEEK_END + 1):
            first = self.subjects_by_weekday[weekday]
            second = schedule.subjects_by_weekday[weekday]
            diff = Diff(first, second)
            diff_for_weekday = diff.diff(flags)
            weekdays[weekday] = diff_for_weekday

        return weekdays


def weekday_schedule(group: str, lessons: List[Lesson]) -> Schedule:
    subjects_by_weekday = {k: [] for k in range(WEEK_START, WEEK_END + 1)}
    for lesson in lessons:
        subjects = lesson.subjects
        for subject in subjects:
            subject.start_time = lesson.start_time
            subject.end_time = lesson.end_time

        for weekday in range(WEEK_START, WEEK_END + 1):
            subjects_by_weekday[weekday].extend(filter(lambda subject: subject.subject_day_index == weekday, subjects))

    return Schedule(group, subjects_by_weekday)
