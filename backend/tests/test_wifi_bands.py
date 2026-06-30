from app.domain.wifi_bands import normalize_band


def test_normalize_band_by_hint() -> None:
    assert normalize_band("2.4GHz") == "2.4GHz"
    assert normalize_band("5g") == "5GHz"
    assert normalize_band("6 GHz") == "6GHz"


def test_normalize_band_by_frequency() -> None:
    assert normalize_band(None, frequency_mhz=2412) == "2.4GHz"
    assert normalize_band(None, frequency_mhz=5500) == "5GHz"
    assert normalize_band(None, frequency_mhz=6115) == "6GHz"


def test_normalize_band_by_channel() -> None:
    assert normalize_band(None, channel=11) == "2.4GHz"
    assert normalize_band(None, channel=44) == "5GHz"
    assert normalize_band(None, channel=181) == "6GHz"
