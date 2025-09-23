from typing import List, Dict

# Встроенный каталог рецептов верхнего слоя (минимальный пример)
RECIPES: List[Dict] = [
  {
    "id": "AC-20-A",
    "name": "Асфальтобетон плотный, тип А",
    "composition_pct": {"щебень": 55, "песок": 30, "мин. порошок": 7, "битум": 6, "добавки": 2},
    "unit_cost_rub_per_m2": 1350.0,
    "applicable": {
      "zones": [1, 2, 3],
      "asphalt_types": ["Плотный и высокоплотный"],
      "categories": [1, 2, 3]
    }
  },
  {
    "id": "AC-20-B",
    "name": "Асфальтобетон плотный, тип Б",
    "composition_pct": {"щебень": 50, "песок": 35, "мин. порошок": 8, "битум": 6, "добавки": 1},
    "unit_cost_rub_per_m2": 1300.0,
    "applicable": {
      "zones": [1, 2, 3, 4],
      "asphalt_types": ["Плотный и высокоплотный"],
      "categories": [1, 2, 3]
    }
  },
  {
    "id": "AC-20-V",
    "name": "Асфальтобетон плотный, тип В",
    "composition_pct": {"щебень": 40, "песок": 40, "мин. порошок": 10, "битум": 6, "добавки": 4},
    "unit_cost_rub_per_m2": 1250.0,
    "applicable": {
      "zones": [2, 3, 4],
      "asphalt_types": ["Плотный"],
      "categories": [2, 3]
    }
  },
  {
    "id": "AC-20-G",
    "name": "Асфальтобетон плотный, тип Г",
    "composition_pct": {"щебень": 0, "песок": 75, "мин. порошок": 12, "битум": 6, "добавки": 7},
    "unit_cost_rub_per_m2": 1200.0,
    "applicable": {
      "zones": [3, 4, 5],
      "asphalt_types": ["Плотный"],
      "categories": [1, 2, 3]
    }
  },
  {
    "id": "AC-20-D",
    "name": "Асфальтобетон плотный, тип Д",
    "composition_pct": {"щебень": 0, "песок": 80, "мин. порошок": 12, "битум": 6, "добавки": 2},
    "unit_cost_rub_per_m2": 1180.0,
    "applicable": {
      "zones": [3, 4, 5],
      "asphalt_types": ["Плотный"],
      "categories": [2, 3]
    }
  },
  {
    "id": "SMA-10",
    "name": "Асфальтобетон щебёночно-мастичный, тип ЩМА-10",
    "composition_pct": {"щебень": 65, "песок": 20, "мин. порошок": 9, "битум": 6, "добавки": 1},
    "unit_cost_rub_per_m2": 1500.0,
    "applicable": {
      "zones": [1, 2, 3, 4, 5],
      "asphalt_types": ["Щебёночно-мастичный"],
      "categories": [1, 2, 3]
    }
  },
  {
    "id": "LA-10",
    "name": "Асфальтобетон литой",
    "composition_pct": {"щебень": 0, "песок": 60, "мин. порошок": 25, "битум": 9, "добавки": 6},
    "unit_cost_rub_per_m2": 1600.0,
    "applicable": {
      "zones": [1, 2, 3],
      "asphalt_types": ["Литой"],
      "categories": [1, 2]
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
