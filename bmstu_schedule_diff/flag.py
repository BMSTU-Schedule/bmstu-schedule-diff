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

from enum import IntFlag, unique


@unique
class Flag(IntFlag):
    SAME_BUILDING = 1 << 0
    SAME_BUILDING_SIDE = 1 << 1
    SAME_START_TIME = 1 << 2
    SAME_END_TIME = 1 << 3
    SAME_FLOOR = 1 << 4
    NEARBY_FLOOR = 1 << 5
    NEARLY_SAME_TIME = 1 << 6
    SAME_AUDITORIUM = 1 << 7
