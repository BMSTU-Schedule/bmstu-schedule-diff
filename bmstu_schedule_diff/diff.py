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

from typing import List, Tuple

from bmstu_schedule import Subject

from .filter import get_filters


class Diff(object):

    def __init__(self, first: List[Subject], second: List[Subject]):
        self.first = first
        self.second = second

    def diff(self, flags: int) -> List[Tuple[Subject, Subject]]:
        matching = []
        for subject1 in self.first:
            for subject2 in self.second:
                if subject1.weeks_interval == subject2.weeks_interval:
                    matches = True
                    for filter in get_filters(flags):
                        if not filter.matches(subject1, subject2):
                            matches = False

                    if matches:
                        matching.append((subject1, subject2))

        return matching
