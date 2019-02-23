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
from typing import Iterator

from .auditorium import valid_auditorium, floors_difference, digits
from .building import building, Building
from .flag import Flag


def get_filters(flags: int) -> Iterator[object]:
    if flags & Flag.SAME_BUILDING:
        differentiate_main_sides = bool(flags & Flag.SAME_BUILDING_SIDE)
        yield SameBuildingFilter(differentiate_main_sides)

    if flags & Flag.SAME_START_TIME:
        yield SameStartTimeFilter()

    if flags & Flag.SAME_END_TIME:
        yield SameEndTimeFilter()

    if flags & Flag.SAME_FLOOR:
        yield SameFloorFilter()

    if flags & Flag.NEARBY_FLOOR:
        yield NearbyFloorFilter()

    if flags & Flag.NEARLY_SAME_TIME:
        yield NearlySameTimeFilter()

    if flags & Flag.SAME_AUDITORIUM:
        yield SameAuditoriumFilter()


class SameBuildingFilter(object):

    def __init__(self, differentiate_main_sides: bool):
        self.differentiate_main_sides = differentiate_main_sides

    def matches(self, subject1, subject2) -> bool:
        if not (valid_auditorium(subject1.auditorium) and valid_auditorium(subject2.auditorium)):
            return False
        b1, b2 = building(subject1, self.differentiate_main_sides), building(subject2, self.differentiate_main_sides)
        return b1 == b2 and b1 != Building.UNKNOWN


class SameStartTimeFilter(object):

    def __init__(self):
        pass

    def matches(self, subject1, subject2) -> bool:
        return subject1.start_time == subject2.start_time


class SameEndTimeFilter(object):

    def __init__(self):
        pass

    def matches(self, subject1, subject2) -> bool:
        return subject1.end_time == subject2.end_time


class SameFloorFilter(object):

    def __init__(self):
        pass

    def matches(self, subject1, subject2) -> bool:
        if not (valid_auditorium(subject1.auditorium) and valid_auditorium(subject2.auditorium)):
            return False
        if floors_difference(digits(subject1.auditorium), digits(subject2.auditorium)) == 0:
            return True
        return False


class NearbyFloorFilter(object):

    def __init__(self):
        pass

    def matches(self, subject1, subject2) -> bool:
        if not (valid_auditorium(subject1.auditorium) and valid_auditorium(subject2.auditorium)):
            return False
        if floors_difference(digits(subject1.auditorium), digits(subject2.auditorium)) <= 1:
            return True
        return False


class SameAuditoriumFilter(object):

    def __init__(self):
        pass

    def matches(self, subject1, subject2) -> bool:
        if not (valid_auditorium(subject1.auditorium) and valid_auditorium(subject2.auditorium)):
            return False
        if subject1.auditorium == subject2.auditorium:
            return True
        return False


class NearlySameTimeFilter(object):

    def __init__(self):
        pass

    def matches(self, subject1, subject2) -> bool:
        if not (valid_auditorium(subject1.auditorium) and valid_auditorium(subject2.auditorium)):
            return False
        max_interval = 30
        if self.difference(subject1.start_time, subject2.start_time) < max_interval:
            return True
        if self.difference(subject1.end_time, subject2.end_time) < max_interval:
            return True
        if self.difference(subject1.end_time, subject2.start_time) < max_interval:
            return True
        if self.difference(subject2.end_time, subject1.start_time) < max_interval:
            return True
        return False

    def difference(self, t1, t2):
        t1_time = self.get_time(t1)
        t2_time = self.get_time(t2)
        return abs(t2_time - t1_time)

    @staticmethod
    def get_time(time):
        time_arr = re.findall('..', time)[:-1]
        h, m = int(time_arr[0]), int(time_arr[1])
        return h * 60 + m
