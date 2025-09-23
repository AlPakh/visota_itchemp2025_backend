from typing import List, Dict

# Встроенный каталог рецептов верхнего слоя (минимальный пример)
RECIPES: List[Dict] = [
    {
        "id": "AC-20-mod",
        "name": "Асфальтобетон плотный, тип А (модиф.)",
        "composition_pct": {"щебень": 48, "песок": 32, "мин. порошок": 7, "битум": 6, "добавки": 7},
        "unit_cost_rub_per_m2": 1350.0,
        "applicable": {
            "zones": [1, 2, 3, 4, 5],
            "asphalt_types": ["Плотный и высокоплотный", "Плотный"],
            "categories": [1, 2, 3, 4, 5]
        }
    },
    {
        "id": "SMA-15",
        "name": "ЩМА-15",
        "composition_pct": {"щебень": 60, "песок": 20, "мин. порошок": 8, "битум": 6, "добавки": 6},
        "unit_cost_rub_per_m2": 1420.0,
        "applicable": {
            "zones": [2, 3, 4, 5],
            "asphalt_types": ["Плотный"],
            "categories": [1, 2, 3, 4, 5]
        }
    },
    {
        "id": "AC-16",
        "name": "Асфальтобетон плотный, тип Б",
        "composition_pct": {"щебень": 45, "песок": 35, "мин. порошок": 8, "битум": 6, "добавки": 6},
        "unit_cost_rub_per_m2": 1280.0,
        "applicable": {
            "zones": [1, 2, 3, 4, 5],
            "asphalt_types": ["Плотный", "Плотный и высокоплотный"],
            "categories": [2, 3, 4, 5]
        }
    }
]


def select_candidates(features: Dict) -> List[Dict]:
    """Фильтрация рецептов по зоне/типу/категории (простая логика)."""
    z = features["zone"]
    at = {2: "Плотный и высокоплотный", 1: "Плотный", 0: "Из холодных смесей"}[features["asphalt_type_code"]]
    c = features["category"]
    return [
        r for r in RECIPES
        if z in r["applicable"]["zones"]
        and at in r["applicable"]["asphalt_types"]
        and c in r["applicable"]["categories"]
    ]
