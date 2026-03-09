# Nutrislice API Notes

## URL Pattern

```
https://{district}.api.nutrislice.com/menu/api/weeks/school/{slug}/menu-type/{type}/{year}/{month}/{day}/
```

| Component | Value | Notes |
|---|---|---|
| `district` | `srvusd` | San Ramon Valley Unified School District |
| `slug` | e.g. `los-cerros-middle` | kebab-case school identifier |
| `type` | `lunch` | or `breakfast`, etc. |
| `year/month/day` | e.g. `2026/02/26` | zero-padded month and day |

### Known School Slugs (SRVUSD)

| School | Slug |
|---|---|
| Los Cerros Middle | `los-cerros-middle` |
| Vista Grande Elementary | `vista-grande-school` |

> Note: Vista Grande's slug is `vista-grande-school`, not `vista-grande-elementary`.
> Verify other schools by trial and error — a 200 response means the slug is valid.

### Example URL

```
https://srvusd.api.nutrislice.com/menu/api/weeks/school/los-cerros-middle/menu-type/lunch/2026/02/26/
```

## Response Structure

The endpoint always returns a **full week** (~7 days), not just the requested day.
Filter `days[]` by `date` to find the target day.

```
{
  start_date        string   "2026-02-23"
  menu_type_id      int
  days[]
    date            string   "2026-02-26"
    menu_items[]
      food
        name          string   "Chicken Teriyaki w/ White Rice"
        food_category string   "entree" | "beverage" | "fruit" | "vegetable"
        description   string
        rounded_nutrition_info { calories, g_fat, mg_sodium, ... }
        serving_size_info      { serving_size_amount, serving_size_unit }
        icons                  { food_icons[], myplate_icons[] }
      category      string   mirrors food.food_category
}
```

### Food Categories

| Category | Contents |
|---|---|
| `entree` | Main dishes — the only category `LunchParser` returns |
| `beverage` | Milk, juice, etc. |
| `fruit` | Fruit options |
| `vegetable` | Vegetable sides |

### Gotchas

- **Dual category field**: Both `menu_item['category']` and `menu_item['food']['food_category']` exist with the same value. Use `food_category` — it's more reliable.
- **Empty days**: Weekends and holidays appear in `days[]` but have `menu_items: []`.
- **Special characters**: Food names can contain `&`, `<`, `>`, and quotes — sanitize before display or speech.
- **No auth required**: The API is publicly accessible with no API key.
- **Response time**: Typically under 1 second.

## Extracting Entrees with `lunch_parser`

```python
from lunch_parser import LunchParser

parser = LunchParser()                             # district defaults to "srvusd"
entrees = parser.get_entrees("Los Cerros Middle")  # date defaults to today
print(parser.format_menu(entrees))
```

## Raw urllib Example

```python
import json
from urllib.request import urlopen
from datetime import datetime

date = datetime(2026, 2, 26)
slug = "los-cerros-middle"
date_str = date.strftime("%Y-%m-%d")

url = (
    f"https://srvusd.api.nutrislice.com/menu/api/weeks/school/{slug}"
    f"/menu-type/lunch/{date.year}/{date.month:02d}/{date.day:02d}/"
)

with urlopen(url, timeout=8) as response:
    data = json.loads(response.read().decode("utf-8"))

for day in data["days"]:
    if day["date"] == date_str:
        entrees = [
            item["food"]["name"]
            for item in day["menu_items"]
            if item.get("food") and item["food"].get("food_category") == "entree"
        ]
        print(entrees)
```

### Sample Output (Feb 26, 2026 — Los Cerros Middle)

```
['Chicken Teriyaki w/ White Rice',
 'Cheese Focaccia Pizza - Secondary',
 'Turkey, Cheddar & Lettuce on Pullman Loaf - MS',
 'Lunch Parfait:  Vanilla Yogurt w/  Sliced Strawberries',
 'Mac Salad Entree']
```
