from temimbo.dataclasses import *



import random

import copy
from typing import Tuple, Optional

#####################################
# Task type helpers
def get_random_examples(task_type: str, domain: str, n: int) -> List[str]:
    mapping = {
        'multiple_choice': [
            'Select the correct answers:\nI am very happy _____ in India. I really miss being there.\na) to live\nb) to have lived\nc) to be lived\nd) to have living',
            'Select the correct answers:\nThey did not reach an agreement ______ their differences.\na) because of\nb) due to\nc) even though\nd) besides'
        ],
        'single_choice': [
            'Select the correct answer:\nHe is working on his computer with his baby next to _____ \na) himself\nb) his\nc) herself\nd) itself',
            'Select the correct answer:\nShe _____ robbed when she left the chocolate factory.\na) were\nb) did\nc) was\nd) forgot',
        ],
        'gap_text': [
            'For instance, on the planet Earth, man had always assumed that he was more a) _____ than dolphins because he had achieved so much—the wheel, New York, wars and so on—whilst all the dolphins had ever done was muck about in the water having a good b) _____. But c) _____, the dolphins had always believed that they were far more intelligent than man—for precisely the same reasons.',
            "There will be no foolish wand-waving or silly incantations in this class. As such, I don't expect many of you to a) _____ the subtle science and exact art that is potion-making. b) _____, for those select few who possess the predisposition, I can teach you how to bewitch the mind and ensnare the senses. I can tell you how to bottle fame, brew glory, and even put a stopper in death. Then again, maybe some of you have come to Hogwarts in possession of abilities so c) _____ that you feel confident enough to not pay attention!"
        ],
        'odd_one_out': [
            'hotel, motel, town-house, condominium, classroom',
            'switching, learning, read, suffering',
        ],
        'word_groups': [
            'Please match the words to the given topics:\nTopics: outside, learning, music\nlist of words: read, tree, study, song, hike, garden, mathematics, dance, guitar, mountain, vocabulary, concert, calculator, orchestra, river',
            'Please match the words to the given topics:\nTopics: technology, politics, university\nlist of words: blockchain, legislation, education, campus, smartphone, virtual reality, research, cybersecurity, student, artificial intelligence, democracy, campaign, professor, diplomacy, government',
        ],
        'match_title': [
            'Text: The town is divided into different sections. In some towns these are regular, extending out from the center of the town like spokes on a wheel, while in others, where space is limited, they are more random. The different areas are further divided into compounds called “ile”. These vary in size considerably from single dwellings to up to thirty houses. They tend to be larger in the North. Large areas are devoted to government administrative buildings. Newer developments such as industrial or commercial areas or apartment housing for civil servants tends to be build on the edge of the town.\nTitles: a) city structures\nb) social developments in america\nc) environmental influences\nd) town ownership',
            "Text: The field of Computer-Assisted Language Learning (CALL) and its subfield of automatic task generation and evaluation have garnered significant attention in recent years. However, an examination of the existing literature reveals a notable gap regarding the incorporation of state-of-the-art machine learning approaches. Specifically, there is a dearth of research exploring the potential of leveraging the newest advancements in machine learning within the context of CALL. Despite the emergence of powerful large language models, such as OpenAI's GPT-3, their utilization in CALL and their application to automatic task generation and evaluation have not received adequate attention. \nTitles: a) Computer assisted language learning\nb) AI in big companys\nc) attention for details\nd) new technologies for teaching in schools",
        ],
        'text_summary': [
            "Johannes Gutenberg (1398 - 1468) was a German goldsmith and publisher who introduced printing to Europe. His introduction of mechanical movable type printing to Europe started the Printing Revolution and is widely regarded as the most important event of the modern period. It played a key role in the scientific revolution and laid the basis for the modern knowledge-based economy and the spread of learning to the masses. Gutenberg many contributions to printing are: the invention of a process for mass-producing movable type, the use of oil-based ink for printing books, adjustable molds, and the use of a wooden printing press. His truly epochal invention was the combination of these elements into a practical system that allowed the mass production of printed books and was economically viable for printers and readers alike. In Renaissance Europe, the arrival of mechanical movable type printing introduced the era of mass communication which permanently altered the structure of society. The relatively unrestricted circulation of information—including revolutionary ideas—transcended borders, and captured the masses in the Reformation. The sharp increase in literacy broke the monopoly of the literate elite on education and learning and bolstered the emerging middle class.",
            "As the purpose of investigating LLS is to foster learning processes and improve language level, research projects often deal with LLS use in relation to language learning proficiency (Khaldieh, 2000; Magogwe and Oliver, 2007; Wu, 2008; Chen, 2009; Liu, 2010; Al-Qahtani, 2013; Platsidou and Kantaridou, 2014; Charoento, 2016; Rao, 2016). The notion of proficiency has been defined and involved in analysis in a multitude of ways by various researchers. Charoento (2016) involved self-ratings, Wu (2008) used the results from language proficiency and achievement tests, Magogwe and Oliver (2007) incorporated language course grades into their analysis of their results. Most studies have shown a positive relationship between LLS and proficiency, but the direction of their connexion was often different. Some researchers have stressed that strategy use was mainly specified by proficiency. More proficient students engaged in LLS more frequently and also employed a broader range of strategies overall compared to less proficient students (Khaldieh, 2000; Wu, 2008; Rao, 2016). Al-Qahtani (2013) and Charoento (2016) demonstrated that successful students mainly used cognitive strategies, while Wu (2008) emphasised significant utilisation of cognitive, metacognitive and social strategies among more proficient university students. Chen (2009) pointed to the use of fewer communication strategies among proficient learners, but noted that they employed them more efficiently than less proficient learners. In addition, Magogwe and Oliver (2007) also established that the basic difference in LLS use between proficient and less proficient learners was that more successful students not only used certain LLS significantly more often, but were also able to select the most adequate strategies depending on the goal of their task."
        ]
    }
    if task_type not in mapping:
        raise NotImplementedError(f'Unkown task type {task_type}')
    return random.sample(mapping[task_type], n)

def convert_task_type_to_text(task_type: str) -> str:
    mapping = {
        'multiple_choice': 'multiple choice with given answer possibilities, there can be multiple correct answers. Generate only one task with four answer possibilities',
        'single_choice': 'single choice with given answer possibilities, only one of the answers is correct. Generate only one task with four answer possibilities',
        'gap_text': 'single gap text with at least 3 gaps (missing words) in it, written with as given in the examples, do not provide answers. Enumerate the gaps with letters. Do not generate anything else but the gap text',
        'odd_one_out': 'odd one out, such that 5 words or phrases are provided, where 1 of them does not fit in. enumerate the list of options. Do not provide the correct answer, just a list of words and a task description',
        'word_groups': 'list of 15 words, with 5 each matching up to only one of 3 provided topics/grammatical oders etc. Provide the list in random order, and the 3 topic seperately',
        'match_title': 'short text, and 4 generated titles, in which 3 do not match text and 1 does',
        'text_summary': 'short text that the reader has to summarize in 5 to 6 sentences. only give a text of at least 250 words and a task description asking the student to write a summary, do not write a summary yourself.'
    }
    if task_type not in mapping:
        raise NotImplementedError(f'Unkown task type {task_type}')
    return mapping[task_type]

#####################################
# Domain helpers
def convert_domain_to_text(domain: str) -> str:
    return domain

#####################################
# Level helpers
def convert_level_to_CEFR_name(level: int) -> str:
    mapping = {
        0: 'A1',
        1: 'A2',
        2: 'B1',
        3: 'B2',
        4: 'C1',
        5: 'C2',
    }
    if level not in mapping:
        raise NotImplementedError(f'Unkown level {level}')
    return mapping[level]

def convert_level_to_CEFR_description(level: int) -> str:
    # https://www.coe.int/en/web/common-european-framework-reference-languages/table-1-cefr-3.3-common-reference-levels-global-scale
    mapping = {
        0: 'Can understand and use familiar everyday expressions and very basic phrases aimed at the satisfaction of needs of a concrete type. Can introduce him/herself and others and can ask and answer questions about personal details such as where he/she lives, people he/she knows and things he/she has. Can interact in a simple way provided the other person talks slowly and clearly and is prepared to help',
        1: 'Can understand sentences and frequently used expressions related to areas of most immediate relevance (e.g. very basic personal and family information, shopping, local geography, employment). Can communicate in simple and routine tasks requiring a simple and direct exchange of information on familiar and routine matters.  Can describe in simple terms aspects of his/her background, immediate environment and matters in areas of immediate need',
        2: 'Can understand the main points of clear standard input on familiar matters regularly encountered in work, school, leisure, etc. Can deal with most situations likely to arise whilst travelling in an area where the language is spoken.  Can produce simple connected text on topics which are familiar or of personal interest. Can describe experiences and events, dreams, hopes & ambitions and briefly give reasons and explanations for opinions and plans',
        3: 'Can understand the main ideas of complex text on both concrete and abstract topics, including technical discussions in his/her field of specialisation. Can interact with a degree of fluency and spontaneity that makes regular interaction with native speakers quite possible without strain for either party. Can produce clear, detailed text on a wide range of subjects and explain a viewpoint on a topical issue giving the advantages and disadvantages of various options',
        4: 'Can understand a wide range of demanding, longer texts, and recognise implicit meaning. Can express him/herself fluently and spontaneously without much obvious searching for expressions. Can use language flexibly and effectively for social, academic and professional purposes. Can produce clear, well-structured, detailed text on complex subjects, showing controlled use of organisational patterns, connectors and cohesive devices',
        5: 'Can understand with ease virtually everything heard or read. Can summarise information from different spoken and written sources, reconstructing arguments and accounts in a coherent presentation. Can express him/herself spontaneously, very fluently and precisely, differentiating finer shades of meaning even in more complex situations',
    }
    if level not in mapping:
        raise NotImplementedError(f'Unkown level {level}')
    return mapping[level]

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
        prompt = "Pretend you are a academic english teacher. Generate a task description, and the task according to the format of the examples. No other text or tasks."
        prompt += f"\nGenerate a {convert_task_type_to_text(task_type)}."
        prompt += f" Generate it for the area of {convert_domain_to_text(domain)} teaching,"
        prompt += f" targeting on {' and '.join(training_goals_subset)}."
        
        if sub_domain:
            prompt += f" Specifically, focus on {sub_domain}."
        
        # Level
        level: int
        if domain == 'vocabulary':
            level = level.vocabulary_level
        elif domain == 'grammar':
            level = level.grammar_level
        elif domain == 'text':
            level = level.text_level
        else:
            raise NotImplementedError(f'Unkown domain {domain}')
        prompt += f'\nAdjust the task dificulty to language level {convert_level_to_CEFR_name(level)} ({convert_level_to_CEFR_description(level)}).'


        # Examples
        n: int
        if task_type == 'text_summary':
            n = 0
        else:
            n = 2

        if n > 0:
            prompt += f"\n\nThe following {'are' if n > 1 else 'is'} {n} {'examples' if n > 1 else 'example'} of how the task should be generated with output format and style:"
            for example in get_random_examples(task_type, domain, n = n):
                prompt += f"\n\n {example}"

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
        The goal of this function is to make the text more "interface-like", telling the user where to click
        TODO: not really implemented for now
        '''
        formatted_output_task = raw_output_task
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

    async def evaluate_learner_answer(self, domain: str, formatted_output_task: str, formated_user_answer: str, task_type: str, sub_domain: Optional[str] = None) -> Tuple[str, bool, TrainingGoals]:
        base_prompt = "Pretend you are an academic english teacher. You are evaluating the learner's answer."
        base_prompt += f"\n\nThis was the given task:\n{formatted_output_task}"
        base_prompt += f"\n\nThis was the student's answer:  '{formated_user_answer}'\n"
        
        
        
        # Correctness
        prompt_correctness = base_prompt + "\nEvaluate the learner's answer for correctness. If the learner's answer was correct, output 'correct'. Otherwise output 'wrong'. Output nothing else.\n"
        prompt_correctness += "\nOutput: "
        raw_output_correctness = self.connector_llm.text_completion(prompt_correctness)
        
        # Training goals
        prompt_goals = base_prompt + f"\nConsider that the answer is {raw_output_correctness}."
        prompt_goals = "\nIf the answer is correct: Output 'No training goals'.\nIf the answer is wrong: You have to return training goals. Output at most one topic each that the student has to practice more according to the answer. There are three categories: vocabulary, grammar and text skills. Write max one per category. Only provide key words."
        prompt_goals += "\nOutput: "
        raw_output_goals = self.connector_llm.text_completion(prompt_goals)
        
        # NL feedback
        prompt_feedback = base_prompt + f"\nConsider that the answer is {raw_output_correctness}."
        prompt_feedback += f"Consider that the learner has to practice more about:\n{raw_output_goals}"
        prompt_feedback += "\nOutput a sensible feedback. If the answer is wrong: Tell the learner brielfy what is wrong, and what they have to practice. Tell the user the correct answer, directly referring to them with 'you'. If the answer is correct, just praise the student. Always be nice and encouraging!"
        prompt_feedback += "\nOutput: "
        raw_output_feedback = self.connector_llm.text_completion(prompt_feedback)

        ############################################
        # parse
        # TODO: the types are wrong, everything is being returned as string
        # We should either implement the parsing here, or change the return types to be `Tuple[str, str, str]` as parse them somewhere else
        
        correctness = raw_output_correctness
        #correctness = False
        training_goals = raw_output_goals
        #training_goals = TrainingGoals(
        #    grammar_goals = ["Use of don't", "Simple past, even though pasts are never simple"],
        #    vocabulary_goals = ['Cat anatomical parts']
        #)
        NL_feedback = raw_output_feedback
        #NL_feedback = 'Oh my darling, your mistakes are comprehensible, but...'
        
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
    async def answer_task(self, formatted_text_output: str, answer) -> str:
        answer = answer
        return answer

    async def choose_export(self) -> str:
        export_type = 'file'
        return export_type

    async def choose_domain(self, domain) -> str:
        domain = domain
        return domain
    
    async def choose_task_type(self, task_type) -> str:
        task_type = task_type
        return task_type
    
    async def choose_sub_domain(self) -> str:
        sub_domain = 'some crazy thing that the professor said'
        return sub_domain

    async def export_task(self):
        #TODO
        pass
