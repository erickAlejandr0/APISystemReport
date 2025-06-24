from pydantic import BaseModel, field_validator
from typing import Optional


class GeoJSONGeometry(BaseModel):
    type: str
    coordinates: list

class GeoJSONFeature(BaseModel):
    type: str = "Feature"
    properties: dict
    geometry: GeoJSONGeometry

    @field_validator('geometry')
    def validate_geometry(cls, v):
        if v.type != "Point":
            raise ValueError("Solo se aceptan puntos geográficos")
        if len(v.coordinates) != 2:
            raise ValueError("Coordenadas inválidas")
        return v

class ReporteRequest(BaseModel):
    geojson: GeoJSONFeature
    usuario: Optional[str] = None
    id_incidente: int