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


def valid_auditorium(auditorium: str) -> bool:
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


def digits(auditorium: str) -> str:
    return re.sub("\D", "", auditorium)


def floors_difference(aud1: str, aud2: str) -> int:
    return abs((int(aud1) // 100) - (int(aud2) // 100))
