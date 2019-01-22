
import pybee


def test_datetime_str():
    now = pybee.datetime.now()
    s = pybee.datetime.to_str(now)
    dt = pybee.datetime.from_str(s)
    assert dt == now


def test_datetime_int():
    now = pybee.datetime.now()
    t = pybee.datetime.to_int(now)
    assert type(t) == int
    dt = pybee.datetime.from_int(t)
    assert dt == now
