from uuid import uuid4
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .schemas import (
    RoadInput, PredictResponse, Recommendation,
    Comparison, ComparisonRow
)
    # mypy: ignore-errors
from .domain import DomainScenario
from .recipes import select_candidates
from .ml_forecaster import predict_many

app = FastAPI(title="RoadLab API")

# Разрешим фронтенду ходить к API (ужесточите список origin'ов в проде)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # замените на список доменов фронтенда в проде
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "FastAPI on Render works!"}


@app.post("/predict", response_model=PredictResponse)
def predict(payload: RoadInput):
    # 1) Заводим данные в доменный класс + нормализуем
    scenario = DomainScenario.from_request(payload)
    features = scenario.to_features()

    # 2) Подбираем кандидатов-рецептов (in-memory)
    candidates = select_candidates(features)
    if not candidates:
        raise HTTPException(status_code=400, detail="Нет подходящих рецептов для выбранных условий.")

    # 3) Нормативный расчёт по каждому рецепту (без заглушек)
    preds = predict_many(features, candidates)

    # 4) Стоимость для участка (упрощённо: м2 = ширина проезжей части * 1000 м)
    area_m2 = scenario.carriageway_width_m * 1000
    enriched: List[Recommendation] = []
    preds_sorted = sorted(preds, key=lambda x: (x["unit_cost_rub_per_m2"] * area_m2))
    for rank, p in enumerate(preds_sorted, start=1):
        cost_total = round(p["unit_cost_rub_per_m2"] * area_m2, 2)
        enriched.append(Recommendation(
            rank=rank,
            recipe_id=p["recipe_id"],
            recipe_name=p["recipe_name"],
            composition_pct=p["composition_pct"],
            unit_cost_rub_per_m2=p["unit_cost_rub_per_m2"],
            estimated_cost_total_rub=cost_total,
            metrics=p["metrics"],
            curves=p["curves"],
            heatmap=p["heatmap"]
        ))

    # 5) Сводная таблица для сравнения
    table = [ComparisonRow(
        recipe_id=r.recipe_id,
        lifetime_y=r.metrics.predicted_lifetime_years,
        wear20_pct=r.metrics.predicted_wear_pct_20y,
        max_def_mm=r.metrics.predicted_max_deformation_mm,
        cost_total=r.estimated_cost_total_rub
    ) for r in enriched]

    comparison = Comparison(
        table=table,
        best_by_cost=min(table, key=lambda x: x.cost_total).recipe_id,
        best_by_lifetime=max(table, key=lambda x: x.lifetime_y).recipe_id
    )

    return PredictResponse(
        scenario_id=f"temp-{uuid4().hex[:5]}",
        top_n=len(enriched),
        recommendations=enriched,
        comparison=comparison
    )
