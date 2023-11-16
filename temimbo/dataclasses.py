from pydantic import BaseModel
from typing import Dict, List

# custom classes
class Level(BaseModel):
    vocabulary_level: float
    grammar_level: float
    text_level: float

class TrainingGoals(BaseModel):
    vocabulary_goals: List[str] = []
    grammar_goals: List[str] = []
    text_goals: List[str] = []


class Profile(BaseModel):
    name: str
    level: Level
    training_goals: TrainingGoals
