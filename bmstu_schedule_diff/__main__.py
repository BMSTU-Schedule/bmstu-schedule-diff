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

import argparse

from bmstu_schedule_diff import weekday_schedule, FLAG_NEAR_FLOOR, FLAG_SAME_START_TIME
from parser import get_schedule
from patch import patch_bmstu_schedule


def main():
    args = vars(argparser().parse_args())
    groups = args['groups']
    lessons_per_group = {}
    for group in groups:
        print("Fetching schedule for", group)
        lessons = get_schedule(group)
        lessons_per_group[group] = lessons

    schedules_for_diff = []
    for group in lessons_per_group.keys():
        schedules_for_diff.append(weekday_schedule(group, lessons_per_group[group]))

    initial = schedules_for_diff[0]
    for schedule in schedules_for_diff[1:]:
        initial = initial.diff(schedule, FLAG_SAME_START_TIME | FLAG_NEAR_FLOOR)

    for key in initial.keys():
        print("Weekday:", key)
        for pair in initial[key]:
            print("(", end="")
            print(pair[0].start_time, pair[0].end_time, pair[0].auditorium, end="")
            print(", ", end="")
            print(pair[1].start_time, pair[1].end_time, pair[1].auditorium, end="")
            print(")", end="")
            print()


def argparser():
    parser = argparse.ArgumentParser(
        description='Display BMSTU schedule diff',
        add_help=True
    )
    parser.add_argument(
        'groups',
        type=str,
        nargs='*',
        help='Group identifier'
    )
    return parser


if __name__ == '__main__':
    patch_bmstu_schedule()
    main()
