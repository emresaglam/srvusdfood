# lunch_parser

A standalone Python module for fetching school lunch menus from the
[Nutrislice](https://www.nutrislice.com/) API. No Alexa, AWS, or
third-party dependencies — pure Python standard library.

## Project Structure

```
alexa-lunch/
├── lunch_parser.py       # LunchParser class
├── test_lunch_parser.py  # Tests and usage examples
└── api-notes.md          # Nutrislice API reference
```

## Supported Schools

| Display Name | District | Nutrislice Slug |
|---|---|---|
| Los Cerros Middle | SRVUSD | `los-cerros-middle` |
| Vista Grande Elementary | SRVUSD | `vista-grande-school` |

## Usage

```python
from lunch_parser import LunchParser

parser = LunchParser()

# Get today's entrees
entrees = parser.get_entrees("Los Cerros Middle")

# Get entrees for a specific date
from datetime import datetime
entrees = parser.get_entrees("Vista Grande Elementary", datetime(2026, 2, 26))

# Format as a natural-language string
print(parser.format_menu(entrees))
# → "lunch includes Chicken Teriyaki w/ White Rice, Cheese Pizza, and Mac Salad"

# List supported schools
print(parser.schools)
# → ['Los Cerros Middle', 'Vista Grande Elementary']
```

### Return values for `get_entrees()`

| Return | Meaning |
|---|---|
| `["Pizza", "Salad", ...]` | Entrees found |
| `[]` | No menu today (weekend / holiday) |
| `None` | Network or HTTP error |

Unknown school names raise `ValueError`.

## Configuration

The district and log level can be set in-code (top of `lunch_parser.py`)
or overridden by environment variables:

| Env var | In-code default | Purpose |
|---|---|---|
| `NUTRISLICE_DISTRICT` | `srvusd` | Nutrislice district ID |
| `LOG_LEVEL` | `INFO` | `DEBUG` / `INFO` / `WARNING` / `ERROR` |

```python
# Explicit district in code
parser = LunchParser(district="srvusd")
```

## Running Tests

```bash
python3 test_lunch_parser.py
```

Tests cover format_menu edge cases, unknown-school error handling,
`_sanitize()` character substitutions, and a live API call for both schools.

## Requirements

- Python 3.9+
- No third-party packages

---
Built with ❤️  for students and parents in San Ramon Valley USD
