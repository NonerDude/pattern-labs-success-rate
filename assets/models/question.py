import re
import typing as t
import logging
logger = logging.getLogger(__name__)

from assets.models.solution import Solution

class AnswerNotFoundError(Exception):
    pass

PROMPT_EXPERIMENTAL_INSTRUCTIONS = ["think creatively", "make sure your answer is correct", "You are an expert at physical interaction questions"]

class Question:
    """
        A question model representing the question with the question's content
        different offered solutions for the LLM
    """
    prompt: str
    question_text: str
    solutions: t.List[Solution]
    answer: str

    PROMPT_WRAPPER = """I will give you a question or sentence to complete and two possible answers. Please answer either A or B, depending on which answer is better. You may write down your reasoning but please write your final answer (either A or B) between the <answer> and </answer> tags
        {question_text}
        A. {solution_a}
        B. {solution_b}
        {experimental_instruction}"""
    PROMPT_ANSWER_PATTERN = "<answer>(.*)?</answer>"

    def __init__(self, question_text: str, solutions: t.List[Solution], answer: str, experimental_instruction: str):
        self.question_text = question_text
        self.solutions = solutions
        self.answer = answer
        self.prompt = self._format_prompt(experimental_instruction=experimental_instruction)
    
    def _format_prompt(self, experimental_instruction=""):
        return self.PROMPT_WRAPPER.format(question_text=self.question_text, solution_a=self.solutions[0].solution_text, solution_b=self.solutions[1].solution_text, experimental_instruction=experimental_instruction)
    
    def extract_llm_answer(self, answer: str):
        """
        Extract actual answer from LLM's full answer

        Args:
            answer (str): full answer given by LLM containing pattern to determine actual answer
            <answer>Actual Answer</answer>

        Raises:
            AnswerNotFoundError: answer does not match expected pattern
        """
        found_answer = re.search(self.PROMPT_ANSWER_PATTERN, answer)
        if found_answer is None:
            logger.warning("Answer does not match regex pattern")
            raise AnswerNotFoundError(f"Answer could not be extracted in received text {answer}")
        found_answer = found_answer.group(1)
        logger.info(f"Found Answer: {found_answer}")
        if found_answer == 'A':
            return self.solutions[0].solution_text
        elif found_answer == 'B':
            return self.solutions[1].solution_text
        raise AnswerNotFoundError(f"Answer could not be extracted in received text {answer}")

