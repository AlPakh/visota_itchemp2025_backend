from typing import Dict, List
import random


def predict_many(features: Dict, recipes: List[Dict]) -> List[Dict]:
    """
    Возвращает список словарей с расчётными метриками по каждому рецепту.
    Здесь — простой синтетический расчёт вместо реальной модели.
    """
    out = []
    base = 10 + (features["speed_kmh"] / 50) + (features["axle_load_ts"] / 5) - (features["flow_heavy_share"] * 5)
    for r in recipes:
        # псевдо-метрики
        lifetime = max(8.0, base + random.uniform(2, 6))
        wear20 = max(20.0, 60 - lifetime * 1.5 + random.uniform(-3, 3))
        def_mm = max(1.0, (100 - lifetime) / 10 + random.uniform(0, 1))

        # кривые
        years = [0, 5, 10, 15, 20]
        wear_curve = [round(wear20 * (t / 20), 1) for t in years]
        def_curve = [round(def_mm * (t / 20) ** 1.2, 2) for t in years]

        # теплокарта 3x6
        x = [0, 20, 40, 60, 80, 100]
        y = [0, 50, 100]
        z = [[round(wear20 * 0.3 + i * 0.6 + j * 0.4, 1) for i in range(len(x))] for j in range(len(y))]

        out.append({
            "recipe_id": r["id"],
            "recipe_name": r["name"],
            "composition_pct": r["composition_pct"],
            "unit_cost_rub_per_m2": r["unit_cost_rub_per_m2"],
            "metrics": {
                "predicted_lifetime_years": round(lifetime, 1),
                "predicted_wear_pct_20y": round(wear20, 1),
                "predicted_max_deformation_mm": round(def_mm, 2)
            },
            "curves": {
                "years": years,
                "wear_pct": wear_curve,
                "deformation_mm": def_curve
            },
            "heatmap": {"x": x, "y": y, "z": z}
        })
    return out
