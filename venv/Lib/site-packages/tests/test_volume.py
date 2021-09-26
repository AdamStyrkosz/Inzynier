import logging
import pytest

from config import NOMICS_API_KEY
from nomics import Nomics

@pytest.fixture
def nomics():
    return Nomics(NOMICS_API_KEY)

def test_get_volume_history(nomics):
    data = nomics.Volume.get_volume_history()
    assert isinstance(data, list)
    assert len(data) > 0