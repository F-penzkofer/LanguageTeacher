from temimbo.dataclasses import *





import copy
from typing import Tuple, Optional

class TaskGenerator():
    '''
    Holds the connection credentails
    Known how to talk to OpenAI using their APIs    
    '''


    def __init__(self, openai_endpoint: str, openai_key: str):
        pass

    async def incorporate_profile_in_task(self, profile: Profile, domain: str) -> Tuple[Level, List[str]]:
        level = profile.level
        
        # Fetch goals for domain
        if domain == 'vocabulary':
            training_goals_subset = profile.training_goals.vocabulary_goals
        elif domain == 'grammar':
            training_goals_subset = profile.training_goals.grammar_goals
        elif domain == 'text':
            training_goals_subset = profile.training_goals.text_goals
        else:
            raise ValueError(f'Invalid domain: {domain}')
        
        # Reduce
        training_goals_subset = training_goals_subset[:2]

        return level, training_goals_subset

    async def generate_prompt(self, level: Level, training_goals_subset: List[str], domain: str, task_type: str, sub_domain: Optional[str] = None) -> str:
        prompt = "Imagine you are a professor. Generate a task for..."
        return prompt
    
    async def generate_task(self, prompt: str) -> list:
        '''
        Returns the raw API output
        It's the role of the Formatter to find out how to parse this shit
        '''
        raw_output = {
            "choices": [
                {
                "finish_reason": "stop",
                "index": 0,
                "message": {
                    "content": "Choose the correct form to complete the sentence.\n\n1. Each of the students ________ passed the final exam.\n\n   a) has\n   b) have\n   c) had\n   d) having\n\n2. The company's profits ________ significantly over the past year.\n\n   a) has increased\n   b) have increased\n   c) has been increasing\n   d) have been increasing\n\n3. Neither of the books ________ a satisfying ending.\n\n   a) has\n   b) have\n   c) had\n   d) having\n\n4. The committee ________ reached a decision on the matter.\n\n   a) has\n   b) have\n   c) had\n   d) having\n\n5. The number of students in the class ________ drastically.\n\n   a) has decreased\n   b) have decreased\n   c) has been decreasing\n   d) have been decreasing",
                    "role": "assistant"
                }
                }
            ],
            "created": 1688569739,
            "id": "chatcmpl-7YyPjeBjB86atk48yCxqrwsbpEsgG",
            "model": "gpt-3.5-turbo-0613",
            "object": "chat.completion",
            "usage": {
                "completion_tokens": 185,
                "prompt_tokens": 58,
                "total_tokens": 243
            }
        }
        return raw_output


class Formater():
    async def output_task_formatting(self, openai_raw_outputs: list) -> str:
        '''
        Parses the things that comes out of OpenAI
        '''
        formatted_output_task = 'Hello user, your task is to fill the gaps of...'
        return formatted_output_task

    async def learner_answer_formatting(self, user_answer: str) -> str:
        return user_answer

    # learners answer formatting
    # output task formatting

class AnswerEvaluator():
    # Holds the connection credentails
    # Known how to talk to OpenAI using their APIs

    def __init__(self, openai_endpoint, openai_key):
        pass

    async def evaluate_learner_answer(self, domain: str, formatted_output_task: str, formated_user_answer: str, task_type: str, sub_domain: Optional[str] = None) -> Tuple[str, bool, TrainingGoals]:
        NL_feedback = "You dumbass, can't you see that..."
        correctness = False
        training_goals = TrainingGoals(
            grammar_goals = ["Use of don't", "Simple past, even though pasts are never simple"],
            vocabulary_goals = ['Cat anatomical parts']
        )
        return NL_feedback, correctness, training_goals

    async def give_feedback(self, NL_feedback: str, correctness: bool) -> str:
        '''
        This is responsible for making things pretty

        MAYBE this will be done together with evaluate_learner_answer
        '''
        eval_summary: str = 'Oh my darling, your mistakes are comprehensible, but...'
        return eval_summary
    
    async def update_learner_profile(self, training_goals: TrainingGoals, profile: Profile) -> Profile:
        new_profile = copy.deepcopy(profile)
        new_profile.training_goals.vocabulary_goals += training_goals.vocabulary_goals
        new_profile.training_goals.grammar_goals += training_goals.grammar_goals
        new_profile.training_goals.text_goals += training_goals.text_goals
        return new_profile






#######################################
# Implementation dependent classes
#######################################
class DatabaseClient():
    def __init__(self, connection_string: str):
        pass

    async def load_profile(self, id: str) -> Profile:
        profile = Profile( # This is just a MOCK, for testing
            name = 'Franzy',
            level = Level( 
                vocabulary_level = 5,
                grammar_level = 7,
                text_level = 3,
            ),
            training_goals = TrainingGoals(
                vocabulary_goals = ['Foods and drinks'],
                grammar_goals = [],
                text_goals = ['Describe delicious things'],
            )
        )
        return profile

    async def save_profile(self, profile: Profile):
        pass

    async def save_conversation(self, conversation_id: str, user_answer: str, formatted_text_output: str):
        pass

class UserInterface():
    async def answer_task(self, formatted_text_output: str) -> str:
        answer = 'I choose A'
        return answer

    async def choose_export(self) -> str:
        export_type = 'file'
        return export_type

    async def choose_domain(self) -> str:
        domain = 'vocabulary'
        return domain
    
    async def choose_task_type(self) -> str:
        task_type = 'multiple-choice'
        return task_type
    
    async def choose_sub_domain(self) -> str:
        sub_domain = 'some crayz thing that the professor said'
        return sub_domain

    async def export_task(self):
        #TODO
        pass
