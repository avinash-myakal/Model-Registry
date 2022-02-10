from typing import List, Dict, Any
from dataclasses import dataclass
import marshmallow_dataclass


@dataclass
class Geometry:
    type: str
    coordinates: List[Any]


@dataclass
class Feature:
    type: str
    geometry: Geometry
    properties: Dict[str, Any]


@dataclass
class FeatureCollection:
    type: str
    features: List[Feature]


FeatureCollectionSchema = marshmallow_dataclass.class_schema(FeatureCollection)