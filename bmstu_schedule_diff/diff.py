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

import re
from enum import unique, IntFlag
from typing import List, Tuple

from bmstu_schedule import Subject

from bmstu_schedule_diff import building, Building


@unique
class Flag(IntFlag):
    SAME_BUILDING = 1 << 1
    SAME_BUILDING_SIDE = 1 << 2
    SAME_START_TIME = 1 << 3
    SAME_END_TIME = 1 << 4
    SAME_FLOOR = 1 << 5
    NEARBY_FLOOR = 1 << 6


class Diff(object):

    def __init__(self, first: List[Subject], second: List[Subject]):
        self.first = first
        self.second = second

    def diff(self, flags: int) -> List[Tuple[Subject, Subject]]:
        matching = []
        for subject1 in self.first:
            for subject2 in self.second:
                if subject1.weeks_interval == subject2.weeks_interval:
                    if flags & Flag.SAME_BUILDING:
                        differentiate_main_sides = flags & Flag.SAME_BUILDING_SIDE
                        if not Diff.same_building(subject1, subject2, bool(differentiate_main_sides)):
                            continue

                    if flags & Flag.SAME_START_TIME:
                        if not Diff.same_start_time(subject1, subject2):
                            continue

                    if flags & Flag.SAME_END_TIME:
                        if not Diff.same_end_time(subject1, subject2):
                            continue

                    if flags & Flag.SAME_FLOOR:
                        if not Diff.same_floor_auditorium(subject1, subject2):
                            continue

                    if flags & Flag.NEARBY_FLOOR:
                        if not Diff.nearby_floor_auditorium(subject1, subject2):
                            continue

                    matching.append((subject1, subject2))

        return matching

    @staticmethod
    def same_building(subject1, subject2, differentiate_main_sides: bool):
        if not (valid_auditorium(subject1.auditorium) and valid_auditorium(subject2.auditorium)):
            return False
        b1, b2 = building(subject1, differentiate_main_sides), building(subject2, differentiate_main_sides)
        return b1 == b2 and b1 != Building.UNKNOWN

    @staticmethod
    def same_start_time(subject1, subject2):
        return subject1.start_time == subject2.start_time

    @staticmethod
    def same_end_time(subject1, subject2):
        return subject1.end_time == subject2.end_time

    @staticmethod
    def same_floor_auditorium(subject1, subject2) -> bool:
        if not (valid_auditorium(subject1.auditorium) and valid_auditorium(subject2.auditorium)):
            return False
        if floors_difference(digits(subject1.auditorium), digits(subject2.auditorium)) == 0:
            return True
        return False

    @staticmethod
    def nearby_floor_auditorium(subject1, subject2) -> bool:
        if not (valid_auditorium(subject1.auditorium) and valid_auditorium(subject2.auditorium)):
            return False
        if floors_difference(digits(subject1.auditorium), digits(subject2.auditorium)) <= 1:
            return True
        return False


def valid_auditorium(auditorium: str):
    if not auditorium:
        return False

    s = auditorium.lower()
    if len(s) == 0:
        return False

    blacklist = ('каф', 'уивц', 'утп', 'лекторий', '/', ',')
    for item in blacklist:
        if item in s:
            return False

    return True


def digits(s: str) -> str:
    return re.sub("\D", "", s)


def floors_difference(aud1: str, aud2: str):
    return abs((int(aud1) // 100) - (int(aud2) // 100))
