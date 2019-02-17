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
import re

from bmstu_schedule_diff import weekday_schedule, FLAG_NEAR_FLOOR, FLAG_SAME_START_TIME
from .parser import get_schedule
from .patch import patch_bmstu_schedule

weekday_mapping = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday'
}


def main():
    patch_bmstu_schedule()
    args = vars(argparser().parse_args())
    groups = set(map(lambda group: group.upper(), args['groups']))
    if len(groups) != 2:
        print("Please specify two different groups.")
        return

    lessons_per_group = {}
    for group in groups:
        print(f"Downloading {group} schedule...")
        lessons = get_schedule(group)

        if not lessons:
            print(f"Failed to download schedule for {group}")
            return

        lessons_per_group[group] = lessons

    schedules_for_diff = []
    for group in lessons_per_group.keys():
        schedules_for_diff.append(weekday_schedule(group, lessons_per_group[group]))

    flags = FLAG_SAME_START_TIME | FLAG_NEAR_FLOOR
    print("Looking for lessons on nearby floors...\n")

    initial = schedules_for_diff[0]
    for schedule in schedules_for_diff[1:]:
        initial = initial.diff(schedule, flags)

    if all(not initial[key] for key in initial.keys()):
        print("Nothing found.")
        return

    for weekday in initial.keys():
        if not initial[weekday]:
            continue
        print(f"{weekday_mapping[weekday]}:")
        for pair in initial[weekday]:
            print(f"({pretty_print_subject(pair[0])}, {pretty_print_subject(pair[1])})")
        print()


def pretty_print_subject(subject):
    def format_time(time):
        return ":".join(re.findall('..', time)[:-1])

    return f"{format_time(subject.start_time)}-{format_time(subject.end_time)} {subject.name} {subject.auditorium}"


def argparser():
    parser = argparse.ArgumentParser(
        description='Display BMSTU schedule diff',
        add_help=True
    )
    parser.add_argument(
        'groups',
        type=str,
        nargs='*',
        help='Group identifiers'
    )
    return parser


if __name__ == '__main__':
    main()
