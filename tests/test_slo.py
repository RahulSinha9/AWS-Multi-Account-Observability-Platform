import pytest
from app.slo import availability, error_budget, burn_rate

def test_availability():
    assert availability(999, 1000) == pytest.approx(0.999)

def test_error_budget():
    assert error_budget(0.999) == pytest.approx(0.001)

def test_burn_rate():
    assert burn_rate(0.999, 0.998) == pytest.approx(2)

def test_invalid_counts():
    with pytest.raises(ValueError):
        availability(10, 5)
