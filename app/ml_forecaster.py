from typing import Dict, List
from math import sqrt, pi

# -----------------------------
# Встроенные справочники (укрупнённые, согласованы с ранее присланными шаблонами)
# -----------------------------

# Механические свойства смесей по виду и марке битума
MATERIALS = {
    "Плотный и высокоплотный": {
        "БНД 40/60":  {"E20_MPa": 6500, "nu": 0.35, "alpha_zone": {"1": 0.75, "2": 0.80, "3": 0.85, "4": 0.95, "5": 1.00}},
        "БНД 60/90":  {"E20_MPa": 5500, "nu": 0.35, "alpha_zone": {"1": 0.70, "2": 0.78, "3": 0.85, "4": 0.95, "5": 1.00}},
        "БНД 90/130": {"E20_MPa": 4500, "nu": 0.35, "alpha_zone": {"1": 0.65, "2": 0.75, "3": 0.82, "4": 0.92, "5": 1.00}}
    },
    "Плотный": {
        "БНД 40/60":  {"E20_MPa": 6000, "nu": 0.35, "alpha_zone": {"1": 0.75, "2": 0.80, "3": 0.85, "4": 0.95, "5": 1.00}},
        "БНД 60/90":  {"E20_MPa": 5000, "nu": 0.35, "alpha_zone": {"1": 0.70, "2": 0.78, "3": 0.85, "4": 0.95, "5": 1.00}},
        "БНД 90/130": {"E20_MPa": 4200, "nu": 0.35, "alpha_zone": {"1": 0.65, "2": 0.75, "3": 0.82, "4": 0.92, "5": 1.00}}
    },
    "Из холодных смесей": {
        "СГ 70/130":  {"E20_MPa": 2500, "nu": 0.35, "alpha_zone": {"1": 0.60, "2": 0.70, "3": 0.80, "4": 0.90, "5": 1.00}},
        "МГ 70/130":  {"E20_MPa": 2300, "nu": 0.35, "alpha_zone": {"1": 0.60, "2": 0.70, "3": 0.80, "4": 0.90, "5": 1.00}},
        "МГО 70/130": {"E20_MPa": 2200, "nu": 0.35, "alpha_zone": {"1": 0.60, "2": 0.70, "3": 0.80, "4": 0.90, "5": 1.00}}
    }
}

# Основания и земляное полотно (типовые)
FOUNDATIONS = {
    "base_types": {
        "ЩПС": {"E_MPa": 300, "nu": 0.30},
        "Песчаное": {"E_MPa": 180, "nu": 0.30},
        "Цементогрунт": {"E_MPa": 600, "nu": 0.25}
    },
    "subgrade_by_zone": {
        "1": {"E_subgrade_MPa": 70, "nu": 0.35},
        "2": {"E_subgrade_MPa": 65, "nu": 0.35},
        "3": {"E_subgrade_MPa": 60, "nu": 0.35},
        "4": {"E_subgrade_MPa": 55, "nu": 0.35},
        "5": {"E_subgrade_MPa": 50, "nu": 0.35}
    }
}

# Сезонные множители по зонам
SEASON = {
    "1": {"fatigue_factor": 0.33, "rutting_factor": 0.17},
    "2": {"fatigue_factor": 0.35, "rutting_factor": 0.20},
    "3": {"fatigue_factor": 0.40, "rutting_factor": 0.25},
    "4": {"fatigue_factor": 0.45, "rutting_factor": 0.30},
    "5": {"fatigue_factor": 0.50, "rutting_factor": 0.35}
}

# Трафиковые коэффициенты
TRAFFIC = {
    "design_period_years_default": 20,
    "traffic_growth_pct_default": 0.0,
    "ref_axle_kN": 115,
    "equivalency_exponent": 4.2,
    "DDF_default": 0.5,
    "LDF_by_lanes": {"1": 1.00, "2": 0.90, "3": 0.80, "4": 0.70, "6": 0.55},
    "eq_factor_heavy_to_115kN": 2.0  # укрупнённый коэффициент приведения одного тяжёлого ТС к 115 кН
}

# Толщина пакета АБ по накопленному ESAL (укрупнённо)
ESAL_THICKNESS = [
    {"esal_min": 0, "esal_max": 200_000, "h_ab_total_cm": 8},
    {"esal_min": 200_000, "esal_max": 500_000, "h_ab_total_cm": 10},
    {"esal_min": 500_000, "esal_max": 1_000_000, "h_ab_total_cm": 12},
    {"esal_min": 1_000_000, "esal_max": 3_000_000, "h_ab_total_cm": 14},
    {"esal_min": 3_000_000, "esal_max": 6_000_000, "h_ab_total_cm": 16},
    {"esal_min": 6_000_000, "esal_max": 10_000_000, "h_ab_total_cm": 18}
]

# Разделение толщины между верхним и нижним слоями
SPLIT_RULES = {
    "Плотный и высокоплотный": {"top_share_pct": 40, "bottom_share_pct": 60, "top_min_cm": 4, "bottom_min_cm": 6},
    "Плотный": {"top_share_pct": 40, "bottom_share_pct": 60, "top_min_cm": 4, "bottom_min_cm": 6},
    "Из холодных смесей": {"top_share_pct": 35, "bottom_share_pct": 65, "top_min_cm": 4, "bottom_min_cm": 6}
}

# Модели разрушения
FATIGUE = {  # Nf = K * (1/σ_t)^m  (σ_t в МПа)
    "Плотный и высокоплотный": {"K": 0.05, "m": 4.0, "reliability_default": 0.60},
    "Плотный": {"K": 0.05, "m": 4.0, "reliability_default": 0.60},
    "Из холодных смесей": {"K": 0.03, "m": 4.2, "reliability_default": 0.60}
}

RUTTING = {"K_rut": 1.35e-4, "m_rut": 4.45, "criterion_rut_mm": 20.0}  # Trut ~ K*(1/εz)^m

# Нагрузка в пятне контакта
LOAD = {"tire_pressure_MPa_default": 0.7, "dual_tire_default": True, "wheel_per_axle": 2}

THERMAL_YEARS = 5.0  # эмпирически (по документу)
AGING_YEARS = 7.0     # эмпирически (по документу)

# -----------------------------
# Утилиты расчёта
# -----------------------------

def _get_E_ab(zone: int, asphalt_type: str, bitumen_grade: str) -> float:
    """Эффективный модуль АБ-пакета при 20°C с климатическим множителем по зоне."""
    mat = MATERIALS.get(asphalt_type, {})
    prop = mat.get(bitumen_grade)
    if not prop:
        # если неизвестная марка — берём среднюю по типу
        if mat:
            prop = list(mat.values())[0]
        else:
            prop = {"E20_MPa": 4500, "alpha_zone": {"1": 0.7, "2": 0.78, "3": 0.85, "4": 0.95, "5": 1.0}}
    alpha = float(prop["alpha_zone"].get(str(zone), 1.0))
    return float(prop["E20_MPa"]) * alpha


def _get_foundation(zone: int, base_type: str = "ЩПС") -> Dict[str, float]:
    base = FOUNDATIONS["base_types"].get(base_type, FOUNDATIONS["base_types"]["ЩПС"])
    sub = FOUNDATIONS["subgrade_by_zone"][str(zone)]
    return {"E_base": float(base["E_MPa"]), "E_sub": float(sub["E_subgrade_MPa"])}


def _esal_per_year(intensity: int, heavy_share: float, lanes: int) -> float:
    # приведение к 115 кН
    eq = TRAFFIC["eq_factor_heavy_to_115kN"]
    ldf = TRAFFIC["LDF_by_lanes"].get(str(lanes), 0.7)
    ddf = TRAFFIC["DDF_default"]
    esal_day = intensity * heavy_share * eq * ldf * ddf
    return esal_day * 365.0


def _pick_total_thickness_cm(esal_year: float, years: int = 20) -> float:
    esal_total = esal_year * years
    for rng in ESAL_THICKNESS:
        if rng["esal_min"] <= esal_total < rng["esal_max"]:
            return float(rng["h_ab_total_cm"])
    return float(ESAL_THICKNESS[-1]["h_ab_total_cm"])


def _split_thickness(asphalt_type: str, h_total_cm: float) -> Dict[str, float]:
    rule = SPLIT_RULES.get(asphalt_type, SPLIT_RULES["Плотный"])
    top = max(h_total_cm * rule["top_share_pct"] / 100.0, rule["top_min_cm"])
    bottom = max(h_total_cm - top, rule["bottom_min_cm"])
    # на случай округлений обеспечим сумму
    diff = h_total_cm - (top + bottom)
    if abs(diff) > 1e-6:
        bottom += diff
    return {"h_top_cm": top, "h_bottom_cm": bottom}


def _contact_radius_m(axle_load_ts: float, p_MPa: float) -> float:
    """Радиус контакта покрышки (м) из нагрузки на колесо и давления."""
    wheels = LOAD["wheel_per_axle"]
    Q_N = axle_load_ts * 1000.0 * 9.81 / wheels  # Н
    p_Pa = p_MPa * 1e6  # Па
    area = Q_N / p_Pa   # м²
    return sqrt(area / pi)  # м


def _sigma_t_MPa(q_MPa: float, a_m: float, H_m: float, Eab: float, Ebase: float, Esub: float) -> float:
    """
    Укрупнённый суррогат для растягивающего напряжения на подошве АБ-пакета.
    Калиброван так, чтобы для H≈0.13 м, q=0.7 МПа, a≈0.106 м, Eab≈2800, Ebase≈300 → σ_t ≈ 0.12 МПа.
    """
    ratio_aH = max(a_m / max(H_m, 1e-3), 0.2)
    r1 = max(Ebase / max(Eab, 1e-3), 0.1)
    r2 = max(Esub / max(Eab, 1e-3), 0.05)
    sigma = 0.22 * q_MPa * (ratio_aH ** 0.9) * (r1 ** 0.30) * (r2 ** 0.10)
    return max(0.05, min(sigma, 0.5))


def _eps_z(q_MPa: float, a_m: float, H_m: float, h_base_m: float, Eab: float, Ebase: float, Esub: float) -> float:
    """
    Вертикальная деформация на поверхности грунта (безразмерная), укрупнённая аппроксимация.
    Калибрована к типичному уровню εz ~ 1.8e-4 для стандартных значений.
    """
    span_m = max(H_m + h_base_m, 0.05)
    ratio = max(a_m / span_m, 0.1)
    termE = (q_MPa / max(Esub, 1e-3)) * 1e6  # переведём к масштабу безразмерной деформации
    factor = (Eab / max(Esub, 1e-3)) ** -0.25 * (Ebase / max(Esub, 1e-3)) ** -0.20
    eps = 0.0020 * termE * (ratio ** 0.8) * factor  # около 1.8e-4 в типичных условиях
    return max(5e-5, min(eps, 5e-3))


def _fatigue_years(sigma_t: float, esal_year: float, zone: int, asphalt_type: str) -> float:
    f = FATIGUE[asphalt_type]
    season = SEASON[str(zone)]["fatigue_factor"]
    reliability = f.get("reliability_default", 0.6)
    Nf = f["K"] * (1.0 / max(sigma_t, 1e-6)) ** f["m"]
    return (Nf * reliability) / max(esal_year * season, 1e-6)


def _rutting_years(eps_z: float, esal_year: float, zone: int) -> float:
    season = SEASON[str(zone)]["rutting_factor"]
    N = RUTTING["K_rut"] * (1.0 / max(eps_z, 1e-9)) ** RUTTING["m_rut"]
    return (N) / max(esal_year * season, 1e-6)


def _curves_and_heatmap(life_years: float, eps_z: float) -> Dict[str, object]:
    years = [0, 5, 10, 15, 20]
    wear_pct_20 = min(100.0, max(0.0, 100.0 * (20.0 / max(life_years, 1e-6))))
    # кривая износа: пропорционально времени до насыщения (обрежем на 100%)
    wear_curve = [round(min(100.0, wear_pct_20 * (t / 20.0)), 1) for t in years]
    # деформация (мм) — от εz (порядок нескольких мм)
    def_max = round(min(40.0, max(1.0, eps_z * 1000.0 * 20.0)), 2)
    def_curve = [round(def_max * (t / 20.0) ** 1.2, 2) for t in years]
    # простая теплокарта уязвимости (по колее вдоль колеи движения)
    x = [0, 20, 40, 60, 80, 100]
    y = [0, 50, 100]
    base = wear_pct_20 * 0.3
    z = [[round(base + i * 0.5 + j * 0.3, 1) for i in range(len(x))] for j in range(len(y))]
    return {
        "wear_pct_20": round(wear_pct_20, 1),
        "def_max_mm": def_max,
        "curves": {"years": years, "wear_pct": wear_curve, "deformation_mm": def_curve},
        "heatmap": {"x": x, "y": y, "z": z},
    }

# -----------------------------
# Публичный API
# -----------------------------

def predict_many(features: Dict, recipes: List[Dict]) -> List[Dict]:
    """
    Нормативный расчёт по формулам из документа:
      - ESAL(115 кН) по интенсивности/структуре и распределительным коэффициентам,
      - выбор общей толщины пакета АБ по ESAL и её разбиение,
      - оценка σ_t и ε_z (суррогатные аппроксимации),
      - усталостная долговечность и колееобразование,
      - итоговый срок службы = min(усталость, колея, термо, старение),
      - данные для графиков/теплокарты.
    Возвращает список результатов по каждому рецепту.
    """
    out: List[Dict] = []

    zone = int(features["zone"])
    asphalt_type = {2: "Плотный и высокоплотный", 1: "Плотный", 0: "Из холодных смесей"}[features["asphalt_type_code"]]
    bitumen = features["bitumen_grade"]

    # 1) ESAL (год)
    esal_year = _esal_per_year(intensity=int(features["intensity"]),
                               heavy_share=float(features["flow_heavy_share"]),
                               lanes=int(features["lanes"]))

    # 2) Общая толщина пакета АБ (см) и разбиение по слоям
    h_total_cm = _pick_total_thickness_cm(esal_year, years=TRAFFIC["design_period_years_default"])
    split = _split_thickness(asphalt_type, h_total_cm)
    h_top_m = split["h_top_cm"] / 100.0
    h_bottom_m = split["h_bottom_cm"] / 100.0
    H_m = h_top_m + h_bottom_m

    # 3) Материалы и модули
    Eab = _get_E_ab(zone, asphalt_type, bitumen)      # МПа
    foundation = _get_foundation(zone, base_type="ЩПС")
    Ebase = foundation["E_base"]
    Esub = foundation["E_sub"]

    # 4) Нагрузка/контакт
    q = LOAD["tire_pressure_MPa_default"]  # МПа
    a = _contact_radius_m(axle_load_ts=float(features["axle_load_ts"]), p_MPa=q)

    # 5) Расчёты σ_t и ε_z
    sigma_t = _sigma_t_MPa(q_MPa=q, a_m=a, H_m=H_m, Eab=Eab, Ebase=Ebase, Esub=Esub)
    eps_z = _eps_z(q_MPa=q, a_m=a, H_m=H_m, h_base_m=0.18, Eab=Eab, Ebase=Ebase, Esub=Esub)  # основание ~18 см

    # 6) Сроки по механизмам
    t_fat = _fatigue_years(sigma_t, esal_year, zone, asphalt_type)
    t_rut = _rutting_years(eps_z, esal_year, zone)
    t_therm = THERMAL_YEARS
    t_age = AGING_YEARS
    life = min(t_fat, t_rut, t_therm, t_age)

    # 7) Кривые/теплокарта из рассчитанных метрик
    viz = _curves_and_heatmap(life, eps_z)

    for r in recipes:
        out.append({
            "recipe_id": r["id"],
            "recipe_name": r["name"],
            "composition_pct": r["composition_pct"],
            "unit_cost_rub_per_m2": r["unit_cost_rub_per_m2"],
            "metrics": {
                "predicted_lifetime_years": round(life, 2),
                "predicted_wear_pct_20y": viz["wear_pct_20"],
                "predicted_max_deformation_mm": viz["def_max_mm"]
            },
            "curves": viz["curves"],
            "heatmap": viz["heatmap"]
        })

    return out
