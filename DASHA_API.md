# Dasha API – Frontend Reference

Dasha (Vimshottari) data is available in two places:

1. **`POST /api/birth-chart`** – response includes a top-level **`dasha`** object.
2. **`POST /api/dasha`** – response is focused on dasha: **`success`**, **`basic_details`**, **`dasha`**, **`input`**.

Use the same request body (name, date, time, latitude, longitude, timezone) for both.

---

## Response shape: `dasha`

When dasha is available (no error), **`dasha`** has:

| Key | Description |
|-----|-------------|
| **`balance`** | `{ "PlanetName": years }` – Balance of the **first** mahadasha at birth (in years). Example: `{"Venus": 9.791}`. |
| **`all`** | Full Vimshottari schedule. See below. |
| **`current`** | Currently running mahadasha(s) and nested antardasha(s), pratyantardasha(s). Same structure as `all` but only current/active. |
| **`upcoming`** | Next mahadasha(s) / antardasha(s). Same structure. |
| **`summary`** | Flat summary for UI. See below. |

If dasha data is missing or fails, **`dasha`** will be `{ "error": "message" }`.

---

## Structure of `all`, `current`, `upcoming`

```
mahadashas: {
  "PlanetName": {
    "start": "YYYY-MM-DD" or "YYYY-MM-DDTHH:MM:SS...",
    "end": "YYYY-MM-DD" or "YYYY-MM-DDTHH:MM:SS...",
    "antardashas": {
      "PlanetName": {
        "start": "...",
        "end": "...",
        "pratyantardashas": {
          "PlanetName": { "start": "...", "end": "..." },
          ...
        }
      },
      ...
    }
  },
  ...
}
```

- **Planet names**: Venus, Sun, Moon, Mars, Rahu, Jupiter, Saturn, Mercury, Ketu (order depends on birth nakshatra).
- All dates are ISO strings (date or datetime).

---

## `summary` – flat fields for current period

| Field | Description |
|-------|-------------|
| **`current_mahadasha`** | Name of current mahadasha (e.g. `"Rahu"`). |
| **`current_mahadasha_start`** | Start date (ISO string). |
| **`current_mahadasha_end`** | End date (ISO string). |
| **`current_antardasha`** | Name of current antardasha (e.g. `"Jupiter"`). |
| **`current_antardasha_start`** | Start date. |
| **`current_antardasha_end`** | End date. |
| **`current_pratyantardasha`** | Name of current pratyantardasha (e.g. `"Saturn"`). |
| **`current_pratyantardasha_start`** | Start date. |
| **`current_pratyantardasha_end`** | End date. |
| **`balance_at_birth_years`** | Same as top-level `balance`: `{ "PlanetName": years }`. |
| **`first_mahadasha_lord`** | Planet that ruled the first mahadasha at birth. |
| **`first_mahadasha_balance_years`** | Balance (years) of that first mahadasha at birth. |

---

## Example: what to show in the Dasha section

- **Current period**: `summary.current_mahadasha` / `current_antardasha` / `current_pratyantardasha` and their `*_start` / `*_end`.
- **Balance at birth**: `summary.balance_at_birth_years` or `dasha.balance`.
- **Full timeline**: Use `dasha.all.mahadashas` to show all mahadashas and, per mahadasha, `antardashas` (and optionally `pratyantardashas`).
- **Upcoming**: Use `dasha.upcoming` to show next periods.

All date strings can be passed to `new Date(...)` or formatted as needed.
