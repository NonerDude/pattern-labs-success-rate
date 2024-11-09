import random
import typing as t
from jsonschema import validate, ValidationError

from assets.loaders.file_loaders.file_lines_reader import FileLinesReader
from assets.loaders.file_loaders.json_list_loader import JSONListLoader
from assets.models.question import Question, PROMPT_EXPERIMENTAL_INSTRUCTIONS
from assets.models.solution import Solution
import logging
logger = logging.getLogger(__name__)

class QuestionParseError(Exception):
    pass

class QuestionBuilder:
    question_schema = {
        "goal": str,
        "sol1": str,
        "sol2": str,
        "answer": int
    }
    def question_from_json(self, question: t.Dict, answer: int, experimental_instruction: str):
        try:
            validate(instance=question, schema=self.question_schema)
        except ValidationError as validation_error:
            logger.error(f"Question json object does not match schema: {validation_error}")
            raise QuestionParseError(validation_error)
        solutions = [question.get("sol1"), question.get("sol2")]
        question_solutions = [Solution(solution_text=solution) for solution in solutions]
        return Question(question_text=question.get("goal"), solutions=question_solutions, answer=solutions[answer], experimental_instruction=experimental_instruction)
        

class QuestionsLoader:
    question_builder: QuestionBuilder
    json_loader: JSONListLoader
    list_loader: FileLinesReader
    experimental_instruction: str

    def __init__(self):
        self.json_loader = JSONListLoader()
        self.list_loader = FileLinesReader()
        self.question_builder = QuestionBuilder()
        self.experimental_instruction = self._generate_experimental_instruction()
        logger.info(f"Using custom instruction {self.experimental_instruction}")

    @staticmethod
    def _generate_experimental_instruction() -> str:
        instructions = [""]
        instructions.extend(PROMPT_EXPERIMENTAL_INSTRUCTIONS)
        return random.choices(instructions, weights=[5, *([1] * len(PROMPT_EXPERIMENTAL_INSTRUCTIONS))], k=1)[0]

    def load(self, questions_path: str, answer_path: str) -> t.List[Question]:
        logger.info("Loading questions")
        questions = []
        for question, answer in zip(self.json_loader.load(questions_path), self.list_loader.read(answer_path)):
            questions.append(self.question_builder.question_from_json(question, answer=int(answer), experimental_instruction=self.experimental_instruction))

        return questions