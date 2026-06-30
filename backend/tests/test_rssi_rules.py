from app.domain.rssi_rules import classify_rssi


def test_classify_rssi_thresholds() -> None:
    assert classify_rssi(-50) == "excellent"
    assert classify_rssi(-55) == "good"
    assert classify_rssi(-67) == "minimum"
    assert classify_rssi(-72) == "weak"
    assert classify_rssi(-80) == "unstable"
