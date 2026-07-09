# Spirit Island Companion App

A personal companion application for **Spirit Island**.

The goal of this project is to generate, record and analyse Spirit Island games.

The application will eventually run on:

- Windows (development)
- Android (APK)
- possibly other platforms later

---

# Features

## Game generation

The application will generate Spirit Island games with:

- 2 to 6 spirits
- random or selected spirits
- random or selected spirit boards
- board configurations:
  - Normal
  - Star
  - Line
  - ...

- board side:
  - Easy
  - Difficult (thematic)

- adversaries:
  - random
  - selected
  - configurable difficulty

- scenarios:
  - random
  - selected

The generator prevents duplicate games by storing a unique game signature.

---

# Game tracking

After playing a generated game, the application can store:

- win/loss result
- score
- comments
- picture of the final board
- picture of the team friends reaction of the win
- date played

---

# Statistics

Future features:

- win rate by spirit
- win rate by adversary
- win rate by configuration
- average scores
- most played spirits
- difficulty analysis

---

# Project structure
SpiritIslandApp/

├── main.py

├── create_database.py

├── engine/
│ ├── database.py
│ ├── generator.py
│ ├── recorder.py
│ ├── constraints.py
│ └── models.py

├── ui/
│ ├── home.py
│ ├── generate.py
│ ├── result.py
│ ├── history.py
│ └── statistics.py

├── assets/
│ ├── spirits/
│ ├── boards/
│ ├── scenarios/
│ └── adversaries/

└── spirit_island.db

# Technology

## Backend

- Python
- SQLite

## Interface

- Kivy

## Mobile packaging

- Buildozer
- Android APK

---

# Development setup

## Clone repository

```bash
git clone <repository-url>
cd SpiritIslandApp