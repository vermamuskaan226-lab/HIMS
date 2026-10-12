# HIMS — Frontend / Backend Split

This package keeps the original HIMS Streamlit application behavior and UI, but separates:
- `frontend.py` — Streamlit pages, styling, navigation, forms, charts and dashboard UI.
- `backend.py` — SQLite database, doctor/patient operations, validation, department assignment, patient registration and business logic.
- `hims.db` — Existing HIMS SQLite database.
- `requirements.txt` — Required Python packages.

## Run

```bash
pip install -r requirements.txt
streamlit run frontend.py
```

## Demo doctors

- RAK001 / 1234
- MAD001 / 1234
- PRI001 / 1234
- ANI001 / 1234

## Architecture

```text
frontend.py
    |
    +---- imports backend.py
             |
             +---- SQLite database (hims.db)
```

The application remains Streamlit-based. No Flask conversion was made.

## Notes

Keep `frontend.py`, `backend.py`, and `hims.db` in the same folder so the database path remains relative to the application directory.
# HIMS
# HIMS
# HIMS
# HIMS
# HIMS
# HIMS
# HIMS
