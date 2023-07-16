from pydantic import BaseModel
from typing import Dict, List

# domain = enum[vocabulary, grammar, text]


class Level(BaseModel):
    vocabulary_level: int
    grammar_level: int
    text_level: int

class TrainingGoals(BaseModel):
    vocabulary_goals: List[str] = []
    grammar_goals: List[str] = []
    text_goals: List[str] = []


class Profile(BaseModel):
    name: str
    level: Level
    training_goals: TrainingGoals
