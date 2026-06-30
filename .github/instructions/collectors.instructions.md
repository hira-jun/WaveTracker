---
applyTo: "collectors/**"
description: "Collector script conventions for WaveTracker offline Wi-Fi survey packaging."
---

# Collectors Instructions

- Support offline capture and local ZIP generation only.
- Keep output contract stable:
  - `metadata.json`
  - `scan.json`
  - `networks.txt`
  - `interface.txt`
  - `logs/`
- Keep scripts platform-specific but output format consistent.
- Do not write personal data fields into payloads.
