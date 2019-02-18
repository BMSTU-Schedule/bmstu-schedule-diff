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

from enum import unique, Enum, auto

from bmstu_schedule import Subject


@unique
class Building(Enum):
    MAIN = auto()
    MAIN_SOUTH = auto()
    MAIN_NORTH = auto()
    ULK = auto()
    MT = auto()
    E = auto()
    M = auto()
    LEKTORIUM = auto()
    KAF = auto()
    UNKNOWN = auto()


def building(subject: Subject, differentiate_main_sides: bool) -> Building:
    if not subject.auditorium:
        return Building.UNKNOWN

    auditorium = subject.auditorium.lower()
    if auditorium.isdigit():
        if differentiate_main_sides:
            return Building.MAIN_NORTH
        return Building.MAIN
    if auditorium[-1:] == 'л':
        return Building.ULK
    if auditorium[-1:] == 'м':
        return Building.M
    if auditorium[-1:] == 'э':
        return Building.E
    if auditorium[-1:] == 'ю':
        if differentiate_main_sides:
            return Building.MAIN_SOUTH
        return Building.MAIN
    if auditorium[-2:] == 'мт':
        return Building.MT
    if auditorium == 'каф':
        return Building.KAF
    if auditorium == 'лекторий':
        return Building.LEKTORIUM
    return Building.UNKNOWN
