from temimbo.dataclasses import *





import copy
from typing import Tuple, Optional

#####################################
# TODO move this?
def get_random_examples(task_type: str, domain: str, n: int) -> List[str]:
    mapping = {
        'multiple_choice': [
            'Example text ____ with gap\na) answer option 1\nb) answer option 2\nc) answer  option 3\nd) answer  option 4',
            'Which ',
        ],
        'single_choice': [
            'Example text ____ with gap\na) answer option 1\nb) answer option 2\nc) answer  option 3\nd) answer  option 4',
            #'lalala',
            #'lololo',
        ],
        'gap_text': [
            'Example text ____ with gap',
        ],
        'odd_one_out': [
            'matching word, matching word, non-matching word, matching word',
            'teach, learn, lecture, show',
            'switching, learning, read, suffering',
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
        'multiple_choice': 'multiple choice (4 possible answer choices per task), there can be multiple correct answers',
        'single_choice': 'single choice (4 possible answer choices per task), only one answer is correct',
        'gap_text': 'gap text, without offered answer possibilites',
        'odd_one_out': 'odd one out, such that 5 words or phrases are provided, where 1 of them does not fit in',
        'word_groups': 'word groups, such that there are 3 topics/grammatical oders etc and 15 words, such that each group has 5 words each',
        'match_title': 'a short text, and 4 generated titles, in which 3 do not match text and 1 does',
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
        prompt += " It should be for academic english learners. Therefore, the tasks have to train academic english!"
        prompt += "\nThe following is an example of how the task should be generated. The language level should be C1 or higher"

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
        # TODO: if there are too many goals, kick out the first ones
        new_profile = copy.deepcopy(profile)
        new_profile.training_goals.vocabulary_goals += training_goals.vocabulary_goals
        new_profile.training_goals.grammar_goals += training_goals.grammar_goals
        new_profile.training_goals.text_goals += training_goals.text_goals
        return new_profile






#######################################
# Implementation dependent classes
#######################################
import json
class DatabaseClient():
    '''
    Abstract object to interface with a data storage
    @param connection_string represents the connection information to the database
    '''
    connection_string: str
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    async def load_profile(self, id: str) -> Profile:
        raise NotImplementedError('This is an abstract method')

    async def save_profile(self, profile: Profile):
        raise NotImplementedError('This is an abstract method')

    async def save_conversation(self, conversation_id: str, user_answer: str, formatted_text_output: str):
        raise NotImplementedError('This is an abstract method')



class DatabaseClientLocalFile(DatabaseClient):
    '''
    connection_string is actually just the path to the local folder used for storage
    not including a trailing /
    '''
    async def load_profile(self, id: str) -> Profile:
        with open(f'{self.connection_string}/profile/{id}.json', 'r') as f:
            content: str = f.read()
        profile = Profile(**json.loads(content))
        return profile

    async def save_profile(self, profile: Profile):
        content: str = json.dumps(profile.dict())
        with open(f'{self.connection_string}/profile/{profile.name}.json', 'w') as f:
            f.write(content)

    async def save_conversation(self, conversation_id: str, user_answer: str, formatted_text_output: str):
        # TODO: this is probably too symplistic
        content: str = json.dumps({
            'conversation_id': conversation_id,
            'user_answer': user_answer,
            'formatted_text_output': formatted_text_output,
        })
        with open(f'{self.connection_string}/profile/{conversation_id}.json', 'w') as f:
            f.write(content)

class DatabaseClientMongoDB(DatabaseClient):
    '''
    pymongo is a required dependency
    pip install pymongo
    '''
    def __init__(self, connection_string: str):
        import pymongo
        self.client = pymongo.MongoClient(connection_string)

    async def load_profile(self, id: str) -> Profile:
        profile = Profile(**dict(self.client.my_db.profile.find_one({'name': id})))
        return profile

    async def save_profile(self, profile: Profile):
        raise NotImplementedError('TODO')

    async def save_conversation(self, conversation_id: str, user_answer: str, formatted_text_output: str):
        raise NotImplementedError('TODO')


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
        sub_domain = 'some crazy thing that the professor said'
        return sub_domain

    async def export_task(self):
        #TODO
        pass
