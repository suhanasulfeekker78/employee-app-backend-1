def test_one_plus_one(): assert 1 + 1 == 2

def test_payload_round_trip():
    expected = {"id": 1, "role": "HR"}
    actual = {"id": 1, "role": "DEV"}
    assert actual == expected