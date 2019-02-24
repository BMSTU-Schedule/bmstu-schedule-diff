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
from typing import Tuple, List, Dict

import requests
from bmstu_schedule import Subject, Lesson

from .flag import Flag
from .parser import get_schedule
from .patch import patch_bmstu_schedule
from .schedule import weekday_schedule


def main():
    patch_bmstu_schedule()
    args = vars(argparser().parse_args())
    groups = set(map(lambda group: group.upper(), args['groups']))
    if len(groups) != 2:
        print("Please specify two different groups.")
        return

    schedules: Dict[str, List[Lesson]] = {}
    for group in groups:
        print(f"Downloading {group} schedule...")
        try:
            schedule = get_schedule(group)
        except requests.exceptions.ConnectionError:
            print(f"Failed to download {group} schedule: network is unreachable.")
            return

        schedules[group] = schedule

    schedules_for_diff = [weekday_schedule(group, schedules[group]) for group in schedules.keys()]
    flags = Flag.SAME_BUILDING | Flag.NEARBY_FLOOR | Flag.NEARLY_SAME_TIME
    print("Looking for close lessons...\n")

    schedule1 = schedules_for_diff[0]
    schedule2 = schedules_for_diff[1]
    diff = schedule1.diff(schedule2, flags)

    print_results(diff)


weekday_mapping = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday'
}


def print_results(results: Dict[int, List[Tuple[Subject, Subject]]]):
    if all(not results[key] for key in results.keys()):
        print("Nothing found.")
        return

    for weekday in results.keys():
        if not results[weekday]:
            continue
        print(f"{weekday_mapping[weekday]}:")
        for pair in results[weekday]:
            print(f"{weeks_interval(pair[0].weeks_interval)} ({pretty_print_subject(pair[0])}, {pretty_print_subject(pair[1])})")
        print()


def weeks_interval(weeks_interval):
    if weeks_interval == 1:
        return "ЧС"
    return "ЗН"


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
