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
from datetime import datetime

parser = LunchParser()

# Full menu grouped by category (entree, beverage, fruit, vegetable, ...)
menu = parser.get_full_menu("Los Cerros Middle")
for category, items in menu.items():
    print(f"{category.upper()}: {', '.join(items)}")
# ENTREE: Chicken Teriyaki w/ White Rice, Cheese Pizza, ...
# FRUIT: Apples, Mandarin, ...
# VEGETABLE: Mixed Greens, Edamame
# BEVERAGE: 1% White Milk, Nonfat White Milk

# Entrees only
entrees = parser.get_entrees("Los Cerros Middle")
print(parser.format_menu(entrees))
# → "lunch includes Chicken Teriyaki w/ White Rice, Cheese Pizza, and Mac Salad"

# Specific date
menu = parser.get_full_menu("Vista Grande Elementary", datetime(2026, 2, 26))

# List supported schools
print(parser.schools)
# → ['Los Cerros Middle', 'Vista Grande Elementary']
```

### Return values

Both `get_full_menu()` and `get_entrees()` follow the same contract:

| Return | Meaning |
|---|---|
| Non-empty result | Menu found |
| `{}` / `[]` | No menu today (weekend / holiday) |
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
