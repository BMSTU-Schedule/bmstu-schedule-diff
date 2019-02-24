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

from typing import List, Dict

import requests
from bmstu_schedule import Lesson

from .display import Display
from .args import argparser
from .flag import Flag
from .parser import get_schedule
from .patch import patch_bmstu_schedule
from .schedule import weekday_schedule


def main():
    display = Display()
    patch_bmstu_schedule()
    args = vars(argparser().parse_args())
    groups = sorted(set(map(lambda group: group.upper(), args['groups'])))
    if len(groups) != 2:
        display.notify_invalid_args()
        return

    schedules: Dict[str, List[Lesson]] = {}
    for group in groups:
        display.notify_downloading(group)
        try:
            schedule = get_schedule(group)
        except requests.exceptions.ConnectionError:
            display.notify_failed_network(group)
            return

        schedules[group] = schedule

    schedules_for_diff = [weekday_schedule(group, schedules[group]) for group in schedules.keys()]
    flags = Flag.SAME_BUILDING | Flag.NEARBY_FLOOR | Flag.NEARLY_SAME_TIME
    display.notify_searching(flags)

    schedule1 = schedules_for_diff[0]
    schedule2 = schedules_for_diff[1]
    diff = schedule1.diff(schedule2, flags)

    display.print_results(schedule1.group, schedule2.group, diff)
    display.destroy()


if __name__ == '__main__':
    main()
