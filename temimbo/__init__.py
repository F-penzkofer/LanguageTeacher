from temimbo.dataclasses import *





import copy
from typing import Tuple, Optional

#####################################
# TODO move this?
def get_random_examples(task_type: str, domain: str, n: int) -> List[str]:
    mapping = {
        'multiple_choice': [
            'Example text ____ with gap\na) answer option 1\nb) answer option 2\nc) answer  option 3\nd) answer  option 4',
            'Example text ____ with gap\na) answer option 1\nb) answer option 2\nc) answer  option 3\nd) answer  option 4',
            'Example text ____ with gap\na) answer option 1\nb) answer option 2\nc) answer  option 3\nd) answer  option 4',
        ],
        'single_choice': [
            'Example text ____ with gap\na) answer option 1\nb) answer option 2\nc) answer  option 3\nd) answer  option 4',
            'lalala',
            'lololo',
        ],
        'gap_text': [
            'Example text ____ with gap',
            'lalala',
            'lololo',
        ],
        'odd_one_out': [
            'odd one out',
            'lalala',
            'lololo',
        ],
        'word_groups': [
            'word groups (free text)',
            'lalala',
            'lololo',
        ],
        'match_title': [
            'match title',
            'lalala',
            'lololo',
        ],
    }
    if task_type not in mapping:
        raise NotImplementedError(f'Unkown task type {task_type}')
    return mapping[task_type][:n]

def convert_task_type_to_text(task_type: str) -> str:
    mapping = {
        'multiple_choice': 'multiple choice (4 possible answer choices per task)',
        'single_choice': 'single choice (4 possible answer choices per task)',
        'gap_text': 'gap text (free text)',
        'odd_one_out': 'odd one out',
        'word_groups': 'word groups (free text)',
        'match_title': 'match title',
    }
    if task_type not in mapping:
        raise NotImplementedError(f'Unkown task type {task_type}')
    return mapping[task_type]

def convert_domain_to_text(domain: str) -> str:
    return domain

###################################
import openai

class ConnectorLLM():
    pass

class ConnectorOpenAI(ConnectorLLM):
    def __init__(self, openai_key: str):
        if openai_key == '':
            raise ValueError('openai_key should be set to a valid key')
        openai.api_key = openai_key
    
    def text_completion(self, prompt: str) -> str:
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": prompt},
            ]
        )
        return response['choices'][0]['message']['content']

###################################
class TaskGenerator():
    '''
    Holds the connection credentails
    Known how to talk to OpenAI using their APIs    
    '''
    def __init__(self, connector_llm: ConnectorLLM):
        self.connector_llm = connector_llm

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
        prompt = "Pretend you are a academic english teacher. Generate only the task itself, no other text."
        prompt += f"\nGenerate a {convert_task_type_to_text(task_type)} task,"
        prompt += f" in the area of {convert_domain_to_text(domain)} teaching,"
        prompt += f" targeting on {' and '.join(training_goals_subset)}."
        # TODO level
        if sub_domain:
            prompt += f" Specifically, focus on {sub_domain}."
        prompt += "\nDo not provide the correct answers, just the task output. Only one task."
        prompt += " It should be for academic english learners."
        prompt += "\nThe following is an example of how the task should be generated."

        for example in get_random_examples(task_type, domain, n = 1):
            prompt += f"\n\n{example}"
        return prompt
    
    async def generate_task(self, prompt: str) -> str:
        '''
        Returns the raw API output
        It's the role of the Formatter to find out how to parse this shit
        '''
        raw_output_task = self.connector_llm.text_completion(prompt)
        return raw_output_task


class Formater():
    async def output_task_formatting(self, raw_output_task: str) -> str:
        '''
        Parses the things that comes out of OpenAI
        '''
        formatted_output_task = 'Hello user, you look pretty today. Now Answer this.\n\n' + raw_output_task
        return formatted_output_task

    async def learner_answer_formatting(self, user_answer: str) -> str:
        return user_answer

    # learners answer formatting
    # output task formatting

class AnswerEvaluator():
    # Holds the connection credentails
    # Known how to talk to OpenAI using their APIs

    def __init__(self, connector_llm: ConnectorLLM):
        self.connector_llm = connector_llm

    async def generate_prompt(self, domain: str, formatted_output_task: str, formated_user_answer: str, task_type: str, sub_domain: Optional[str] = None) -> str:
        prompt = "Pretend you are an academic english teacher. You have three tasks:\nEvaluate the following answer of a student to a given task with boolean values."
        prompt += "\nName the topic the student has to practice more."
        prompt += "\nGive sensible feedback to the student. Tell them what is wrong, and what they have to practice."
        prompt += f"\n\nThis was the given task:\n{formatted_output_task}"
        prompt += f"\n\nThis was the student's answer: \n{formated_user_answer}"
        return prompt

    async def evaluate_learner_answer(self, prompt: str) -> Tuple[str, bool, TrainingGoals]:
        # TODO call opeanai with prompt, parse the 3 variables 
        NL_feedback = 'Oh my darling, your mistakes are comprehensible, but...'
        correctness = False
        training_goals = TrainingGoals(
            grammar_goals = ["Use of don't", "Simple past, even though pasts are never simple"],
            vocabulary_goals = ['Cat anatomical parts']
        )
        return NL_feedback, correctness, training_goals
    
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
        task_type = 'single_choice'
        return task_type
    
    async def choose_sub_domain(self) -> str:
        sub_domain = 'some crayz thing that the professor said'
        return sub_domain

    async def export_task(self):
        #TODO
        pass
