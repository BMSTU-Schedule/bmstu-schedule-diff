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

from typing import List, Dict, Tuple

from bmstu_schedule import Lesson, Subject

FLAG_SAME_START_TIME = 1 << 2
FLAG_SAME_END_TIME = 1 << 3
FLAG_SAME_FLOOR = 1 << 4
FLAG_NEAR_FLOOR = 1 << 5


class Schedule(object):

    def __init__(self, group: str, subjects_by_weekday: Dict[int, List[Subject]]):
        self.group = group
        self.subjects_by_weekday = subjects_by_weekday

    def diff(self, schedule, flags: int) -> Dict[int, List[Tuple[Subject, Subject]]]:
        weekdays = {}

        for weekday in range(0, 6):
            first = self.subjects_by_weekday[weekday]
            second = schedule.subjects_by_weekday[weekday]
            diff = Diff(first, second)
            diff_for_weekday = diff.diff(flags)
            weekdays[weekday] = diff_for_weekday

        return weekdays


def weekday_schedule(group: str, lessons: List[Lesson]) -> Schedule:
    filtered = {}
    for i in range(0, 6):
        filtered[i] = []

    for lesson in lessons:
        subjects = lesson.subjects
        for subject in subjects:
            subject.start_time = lesson.start_time
            subject.end_time = lesson.end_time
        for i in range(0, 6):
            n = filter(lambda x: x.subject_day_index == i, subjects)
            filtered[i].extend(n)

    return Schedule(group, filtered)


class Diff(object):

    def __init__(self, first: List[Subject], second: List[Subject]):
        self.first = first
        self.second = second

    def diff(self, flags: int) -> List[Tuple[Subject, Subject]]:
        matching = []
        for subject1 in self.first:
            for subject2 in self.second:
                if subject1.weeks_interval == subject2.weeks_interval:
                    if flags & FLAG_SAME_START_TIME:
                        if not Diff.has_same_start_time(subject1, subject2):
                            continue

                    if flags & FLAG_SAME_END_TIME:
                        if not Diff.has_same_end_time(subject1, subject2):
                            continue

                    if flags & FLAG_SAME_FLOOR:
                        if not Diff.has_same_floor_auditorium(subject1, subject2):
                            continue

                    if flags & FLAG_NEAR_FLOOR:
                        if not Diff.has_same_floor_auditorium(subject1, subject2):
                            continue

                    matching.append((subject1, subject2))

        return matching

    @staticmethod
    def has_same_start_time(subject1, subject2):
        return subject1.start_time == subject2.start_time

    @staticmethod
    def has_same_end_time(subject1, subject2):
        return subject1.end_time == subject2.end_time

    @staticmethod
    def has_same_floor_auditorium(subject1, subject2) -> bool:
        if not (subject1.auditorium and subject2.auditorium):
            return False
        if subject1.auditorium[0] == subject2.auditorium[0]:
            return True
        return False

    @staticmethod
    def has_near_floor_auditorium(subject1, subject2) -> bool:
        if not (subject1.auditorium and subject2.auditorium):
            return False
        if abs(int(subject1.auditorium[0]) - int(subject2.auditorium[0])) <= 1:
            return True
        return False
