import pytest

from bmstu_schedule_diff.building import Building, building_by_auditorium


@pytest.mark.parametrize("auditorium, building", [("112л", Building.ULK), ("312ю", Building.MAIN_SOUTH)])
def test_building(auditorium, building):
    assert building_by_auditorium(auditorium, differentiate_main_sides=True) == building