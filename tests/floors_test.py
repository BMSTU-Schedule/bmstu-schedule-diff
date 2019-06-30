import pytest

from bmstu_schedule_diff.auditorium import auditorium_floor


@pytest.mark.parametrize("auditorium, floor", [("112", 1), ("220", 2), ("1031", 10)])
def test_auditorium_floor(auditorium, floor):
    assert auditorium_floor(auditorium) == floor
