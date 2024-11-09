from langchain_google_genai import ChatGoogleGenerativeAI
from google.generativeai.types.generation_types import StopCandidateException

from assets.models.question import Question
import logging
logger = logging.getLogger(__name__)

class AnswerStopped(Exception):
    pass

class LLM_API:
    MODEL = "gemini-pro"
    api_key: str
    llm: ChatGoogleGenerativeAI

    def __init__(self, api_key: str):
        self.api_key = api_key
        self._init_api()

    def _init_api(self):
        self.llm = ChatGoogleGenerativeAI(
            model=self.MODEL,
            google_api_key=self.api_key,
        )


    def ask(self, question: Question) -> str:
        """
        Function to ask the LLM a Question

        Args:
            question (Question): The question to be asked to the llm, with the different solutions and the correct answer

        Returns:
            str: LLM's answer text
        """
        logger.info(f"Asking LLM Question: {question.prompt}")
        try:
            answer = self.llm.invoke(question.prompt).content
            logger.info(f"Recevied answer: {answer}")
            return question.extract_llm_answer(answer=answer)
        except StopCandidateException as stop_candidate_exception:
            raise AnswerStopped("Answer stopped by API")

