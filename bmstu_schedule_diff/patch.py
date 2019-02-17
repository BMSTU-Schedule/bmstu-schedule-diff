# bmstu-schedule-diff
# Copyright (C) 2018 BMSTU Schedule (George Gabolaev)
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

from datetime import timedelta

import bmstu_schedule


def patch_bmstu_schedule():
    patch_logger()
    patch_subject()


def patch_subject():
    def __init__(self, info, subject_day_index, weeks_interval, denominator):
        self.start_time = None
        self.end_time = None
        self.subject_day_index = subject_day_index
        self.type, self.name, self.auditorium, self.professor = info

        time_shift = denominator * 7 + subject_day_index
        self.start_date = (
                self.semester_start_date + timedelta(days=time_shift)
        ).strftime('%Y%m%d')
        self.weeks_interval = weeks_interval

    bmstu_schedule.Subject.__init__ = __init__


def patch_logger():
    def __fake_logger__(msg):
        pass

    bmstu_schedule.AwesomeLogger.info = __fake_logger__
