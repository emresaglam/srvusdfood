# Nutrislice API Documentation

## API URL Pattern

```
https://{district}.api.nutrislice.com/menu/api/weeks/school/{school-slug}/menu-type/{menu-type}/{year}/{month}/{day}/
```

### Components:
- **district**: `srvusd` (San Ramon Valley Unified School District)
- **school-slug**: `los-cerros-middle` (kebab-case school name)
- **menu-type**: `lunch` (could also be breakfast, etc.)
- **date**: `year/month/day` format (e.g., `2026/02/26`)

### Example URL:
```
https://srvusd.api.nutrislice.com/menu/api/weeks/school/los-cerros-middle/menu-type/lunch/2026/02/26/
```

## Changing Parameters

### Change the Date
Simply modify the year/month/day components:
```
.../2026/02/26/  →  .../2026/03/15/
```

### Change the School
Replace the school slug:
```
.../school/los-cerros-middle/...  →  .../school/pine-valley-middle/...
```
(Note: School slugs are kebab-case versions of school names)

### Change the Menu Type
Replace `lunch` with other meal types:
```
.../menu-type/lunch/...  →  .../menu-type/breakfast/...
```

## JSON Structure

### Top Level
```json
{
  "start_date": "2026-02-23",
  "menu_type_id": 15026,
  "days": [...],
  "id": ...,
  "last_updated": ...,
  "bold_all_entrees_enabled": ...
}
```

### days[] Array
Each day object contains:
```json
{
  "date": "2026-02-26",
  "has_unpublished_menus": false,
  "menu_info": { ... },
  "menu_items": [...]
}
```

### menu_items[] Array
Each menu item contains:
```json
{
  "id": 175134629,
  "position": 0,
  "food": {
    "id": 2106212,
    "name": "Chicken Teriyaki w/ White Rice",
    "description": "",
    "food_category": "entree",
    "rounded_nutrition_info": { ... },
    "serving_size_info": { ... },
    "icons": { ... },
    ...
  },
  "category": "entree",
  ...
}
```

### food Object Fields (Key Fields)
- `id`: Unique food ID
- `name`: Display name of the food item
- `food_category`: Category (e.g., "entree", "beverage", "fruit", "vegetable")
- `description`: Additional description
- `rounded_nutrition_info`: Nutrition data (calories, fat, sodium, etc.)
- `serving_size_info`: Serving size details
- `icons`: Allergen and dietary icons

### Food Categories Observed
- `entree`: Main dishes
- `beverage`: Drinks (milk, etc.)
- `fruit`: Fruit options
- `vegetable`: Vegetable sides

## Python Code to Extract Entree Names

### Complete Example
```python
import json
import urllib.request
from datetime import datetime

def get_entrees(school_slug, date):
    """
    Get entree names for a specific school and date.

    Args:
        school_slug: School identifier (e.g., 'los-cerros-middle')
        date: Date string in 'YYYY-MM-DD' format (e.g., '2026-02-26')

    Returns:
        List of entree names
    """
    # Parse date
    dt = datetime.strptime(date, '%Y-%m-%d')
    year, month, day = dt.year, dt.month, dt.day

    # Build URL
    url = f'https://srvusd.api.nutrislice.com/menu/api/weeks/school/{school_slug}/menu-type/lunch/{year}/{month:02d}/{day:02d}/'

    # Fetch data
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())

    # Find the specific date in days array
    for day_obj in data['days']:
        if day_obj['date'] == date:
            # Extract entrees
            entrees = []
            for menu_item in day_obj['menu_items']:
                if menu_item.get('food'):
                    food = menu_item['food']
                    if food.get('food_category') == 'entree':
                        entrees.append(food['name'])
            return entrees

    return []  # No menu found for this date

# Usage example
entrees = get_entrees('los-cerros-middle', '2026-02-26')
for entree in entrees:
    print(entree)
```

### Output (Feb 26, 2026):
```
Chicken Teriyaki w/ White Rice
Cheese Focaccia Pizza - Secondary
Turkey, Cheddar & Lettuce on Pullman Loaf - MS
Lunch Parfait:  Vanilla Yogurt w/  Sliced Strawberries
Mac Salad Entree
```

### Simplified One-Liner Path
```python
entrees = [
    item['food']['name']
    for day in data['days']
    if day['date'] == target_date
    for item in day['menu_items']
    if item.get('food') and item['food'].get('food_category') == 'entree'
]
```

## Key Insights

1. **API returns a week**: The endpoint returns ~7 days of menu data, not just a single day
2. **Date filtering needed**: You must filter the `days[]` array to find your target date
3. **Empty days exist**: Some days (like weekends) have empty `menu_items[]` arrays
4. **Dual category fields**: Both `item['category']` and `item['food']['food_category']` exist; use `food_category` for reliability
5. **Multiple entrees**: A single day can have 5+ entree options

## Testing the API

The API was tested on 2026-02-26 with the following results:
- Total days returned: 7 (Feb 22-28, 2026)
- Feb 26 had 13 total menu items
- 5 entrees, 2 beverages, 4 fruits, 2 vegetables
- No authentication required
- Response time: Fast (<1 second)
