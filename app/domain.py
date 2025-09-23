from dataclasses import dataclass
from typing import Dict
from .schemas import RoadInput, AsphaltType


@dataclass
class DomainScenario:
    zone: int
    asphalt_type: AsphaltType
    category: int
    bitumen_grade: str

    intensity: int
    flow_heavy_share: float   # 0..1 (из %)
    speed_kmh: int
    axle_load_ts: int

    earthwork_width_m: int
    carriageway_width_m: int
    lanes: int

    @classmethod
    def from_request(cls, req: RoadInput) -> "DomainScenario":
        return cls(
            zone=req.zone,
            asphalt_type=req.asphalt_type,
            category=req.category,
            bitumen_grade=req.bitumen_grade,

            intensity=req.intensity,
            flow_heavy_share=req.flow_structure_pct / 100.0,
            speed_kmh=req.speed,
            axle_load_ts=req.axle_load,

            earthwork_width_m=req.earthwork_width,
            carriageway_width_m=req.carriageway_width,
            lanes=req.lanes
        )

    def to_features(self) -> Dict:
        asphalt_map = {
            AsphaltType.dense_high: 2,
            AsphaltType.dense: 1,
            AsphaltType.cold_mix: 0
        }
        return {
            "zone": self.zone,
            "asphalt_type_code": asphalt_map[self.asphalt_type],
            "category": self.category,
            "bitumen_grade": self.bitumen_grade,

            "intensity": self.intensity,
            "flow_heavy_share": self.flow_heavy_share,
            "speed_kmh": self.speed_kmh,
            "axle_load_ts": self.axle_load_ts,

            "earthwork_width_m": self.earthwork_width_m,
            "carriageway_width_m": self.carriageway_width_m,
            "lanes": self.lanes
        }
