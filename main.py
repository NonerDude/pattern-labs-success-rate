import random



from assets.loaders.questions_loader import QuestionsLoader
from assets.models.question import AnswerNotFoundError
from utils.cli_args_parser import CLIArgParser
from llm_apis.llm_api import LLM_API, AnswerStopped
import logging
import os
LOGGER_FILE = "log.log"
logger = logging.getLogger(__name__)
try:
    os.remove(LOGGER_FILE)
except FileNotFoundError:
    pass
logging.basicConfig(filename=LOGGER_FILE, level=logging.INFO)

class NoSuccessfullRuns(Exception):
    pass

def main():
    args = CLIArgParser().parse_args()
    llm = LLM_API("AIzaSyBGMvrSsc16gkn0iOfapgRmFJfhpTr2PtM")
    chosen_questions = random.choices(QuestionsLoader().load(args.questions_file, args.answers_file), k=args.count_questions)
    logger.info(f"Chose {args.count_questions} questions to ask LLM")
    correct_count = 0
    incorrect_count = 0
    for question in chosen_questions:
        try:
            answer = llm.ask(question=question)
            logger.info(f"Received answer from LLM: {answer}")
            logger.info(f"Expected answer: {question.answer}")
            if (answer == question.answer):
                correct_count += 1
            else:
                incorrect_count += 1
        except AnswerNotFoundError as answer_not_found:
            logger.warning(f"Answer not found in LLM's answer: {answer_not_found}")
        except AnswerStopped as answer_stopped:
            logger.error("Question was stopped")
            raise answer_stopped
    if not correct_count and not incorrect_count:
        raise NoSuccessfullRuns("No successfull api calls")
    success_rate = 100.0 * correct_count / (correct_count + incorrect_count)
    logger.info(f"Success rate calculated: {success_rate}")
    print(success_rate)
    
if __name__ == "__main__":
    main()


