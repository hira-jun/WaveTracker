def classify_rssi(signal_dbm: int) -> str:
    if signal_dbm >= -50:
        return "excellent"
    if signal_dbm >= -60:
        return "good"
    if signal_dbm >= -67:
        return "minimum"
    if signal_dbm >= -75:
        return "weak"
    return "unstable"
