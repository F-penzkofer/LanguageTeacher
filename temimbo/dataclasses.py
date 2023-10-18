from pydantic import BaseModel
from typing import Dict, List

# domain = enum[vocabulary, grammar, text]
# task types = enum[multiple_choice, single_choice, gap_text, odd_one_out, word_groups, match_title]


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
