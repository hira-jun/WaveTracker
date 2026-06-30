---
name: wavetracker-phase0
description: "Use when working on WaveTracker FastAPI backend, React frontend, Wi-Fi collectors, or infra harness. Covers scaffold conventions, xNorm/yNorm coordinate handling, ZIP survey data contract, and Blob/Table storage separation."
---

# WaveTracker Phase0 Skill

## Purpose

Guide implementation for the WaveTracker repository with shared, domain-aware defaults.

## Use This Skill For

- Backend scaffolding with FastAPI and clear route boundaries
- Frontend map-centric UI scaffolding with normalized coordinates
- Collector script templates and ZIP payload contract
- Local infra harness with compose-driven startup and health checks

## Domain Rules

- Preserve storage separation: raw ZIP as Blob-like payload, parsed records as Table-like entities.
- Normalize click coordinates on floor map:
  - xNorm = x / width
  - yNorm = y / height
- Keep collector flow offline-first and upload later.
- Avoid storing personal data; hash hostname if needed.

## Expected Repository Areas

- `backend/`
- `frontend/`
- `collectors/`
- `infra/`
- `docs/`
