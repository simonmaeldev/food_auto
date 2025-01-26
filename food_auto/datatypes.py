from datetime import timedelta
from typing import Dict, List, Optional

from pydantic import BaseModel


class Ingredient(BaseModel):
    url: Optional[str] = None
    name: str
    quantity: Optional[float] = None
    unit: Optional[str] = None


class Macros(BaseModel):
    kcal: int
    proteins: float
    carbs: float
    fat: float


class Recipe(BaseModel):
    name: str
    absolute_path: str
    nb_portions: int
    prep_time: timedelta
    cooking_time: timedelta
    ingredients: List[Ingredient]
    ustensiles: List[str]
    instructions: List[str]
    macros: Macros


class GroceryItem(BaseModel):
    name: str
    url: Optional[str] = None
    quantities: Dict[str, float] = {}
