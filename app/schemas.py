from enum import Enum
from typing import Dict, List
from pydantic import BaseModel, Field, conint, confloat


class AsphaltType(str, Enum):
    dense_high = "Плотный и высокоплотный"
    dense = "Плотный"
    cold_mix = "Из холодных смесей"


class RoadInput(BaseModel):
    # 1) Конструкция ДО
    zone: conint(ge=1, le=5) = Field(..., description="Дорожно-климатическая зона (1-5)")
    asphalt_type: AsphaltType = Field(..., description="Вид асфальтобетона")
    category: conint(ge=1, le=5) = Field(..., description="Категория дороги (1-5)")
    bitumen_grade: str = Field(..., description="Марка битума (напр. 'БНД 60/90')")

    # 2) Нагрузка
    intensity: conint(ge=0) = Field(..., description="Интенсивность движения, авт/сут")
    flow_structure_pct: conint(ge=0, le=100) = Field(..., description="Доля тяжёлых ТС, %")
    speed: conint(ge=0) = Field(..., description="Средняя скорость, км/ч")
    axle_load: conint(ge=0) = Field(..., description="Осевая нагрузка, тс")

    # 3) Пространственные данные
    earthwork_width: conint(ge=1) = Field(..., description="Ширина земляного полотна, м")
    carriageway_width: conint(ge=1) = Field(..., description="Ширина проезжей части, м")
    lanes: conint(ge=1) = Field(..., description="Число полос")


class Curves(BaseModel):
    years: List[conint(ge=0)]
    wear_pct: List[confloat(ge=0)]
    deformation_mm: List[confloat(ge=0)]


class Heatmap(BaseModel):
    x: List[confloat(ge=0)]
    y: List[confloat(ge=0)]
    z: List[List[confloat(ge=0)]]


class Metrics(BaseModel):
    predicted_lifetime_years: confloat(ge=0)
    predicted_wear_pct_20y: confloat(ge=0)
    predicted_max_deformation_mm: confloat(ge=0)


class Recommendation(BaseModel):
    rank: conint(ge=1)
    recipe_id: str
    recipe_name: str
    composition_pct: Dict[str, confloat(ge=0, le=100)]
    unit_cost_rub_per_m2: confloat(ge=0)
    estimated_cost_total_rub: confloat(ge=0)
    metrics: Metrics
    curves: Curves
    heatmap: Heatmap


class ComparisonRow(BaseModel):
    recipe_id: str
    lifetime_y: confloat(ge=0)
    wear20_pct: confloat(ge=0)
    max_def_mm: confloat(ge=0)
    cost_total: confloat(ge=0)


class Comparison(BaseModel):
    table: List[ComparisonRow]
    best_by_cost: str
    best_by_lifetime: str


class PredictResponse(BaseModel):
    scenario_id: str
    top_n: conint(ge=1)
    recommendations: List[Recommendation]
    comparison: Comparison
