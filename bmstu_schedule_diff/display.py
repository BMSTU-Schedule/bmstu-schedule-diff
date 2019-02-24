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
from typing import Tuple, List, Dict

import colorama
from bmstu_schedule import Subject
from colorama import Fore, Style


class Display(object):

    def __init__(self):
        colorama.init(autoreset=True)

    def destroy(self):
        colorama.deinit()

    def info(self, msg: str):
        print(msg)

    def error(self, msg: str):
        print(Fore.RED + msg)

    def notify_invalid_args(self):
        self.error("Please specify two different groups.")

    def notify_downloading(self, group):
        self.info(f"Downloading {group} schedule...")

    def notify_failed_network(self, group):
        self.error(f"Failed to download {group} schedule: network is unreachable.")

    def notify_searching(self, flags):
        self.info("Looking for close lessons...\n")

    def print_results(self, group1, group2, results: Dict[int, List[Tuple[Subject, Subject]]]):
        if all(not results[key] for key in results.keys()):
            self.error("Nothing found.")
            return

        max_length_1 = 0
        max_length_2 = 0
        for weekday in results.keys():
            if not results[weekday]:
                continue
            for pair in results[weekday]:
                subject1 = pretty_print_subject(pair[0])
                subject2 = pretty_print_subject(pair[1])
                if len(subject1) > max_length_1:
                    max_length_1 = len(subject1)
                if len(subject2) > max_length_2:
                    max_length_2 = len(subject2)

        print(f"{Style.BRIGHT}{' ' * 5}{group1.center(max_length_1)}{Style.RESET_ALL}",
              f"{Style.BRIGHT} {group2.center(max_length_2)}{Style.RESET_ALL}")

        for weekday in results.keys():
            if not results[weekday]:
                continue
            print(Style.BRIGHT + f"{WEEKDAYS[weekday]}:")

            for pair in results[weekday]:
                interval = weeks_interval(pair[0].weeks_interval)
                subject1 = pretty_print_subject(pair[0])
                subject2 = pretty_print_subject(pair[1])
                print(interval, color_subject(subject1.ljust(max_length_1)),
                      color_subject(subject2.ljust(max_length_2)))

        print()


def pretty_print_subject(subject):
    def format_time(time):
        return ":".join(re.findall('..', time)[:-1])

    return f"{format_time(subject.start_time)}-{format_time(subject.end_time)} {subject.name} {subject.auditorium}"


def color_subject(subject: str):
    return f"{colorama.Back.LIGHTCYAN_EX} {subject} {colorama.Back.RESET}"


def weeks_interval(weeks_interval):
    if weeks_interval == 1:
        return Fore.LIGHTWHITE_EX + colorama.Back.GREEN + " ЧС " + colorama.Fore.RESET + colorama.Back.RESET
    return Fore.LIGHTWHITE_EX + colorama.Back.BLUE + " ЗН " + colorama.Fore.RESET + colorama.Back.RESET


WEEKDAYS = (
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday'
)
