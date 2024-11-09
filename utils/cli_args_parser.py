
from argparse import ArgumentParser

class Args:
    count_questions: int
    questions_file: str
    answers_file: str


class CLIArgParser():
    arg_parser: ArgumentParser

    prog="LLMTester"
    description="Test LLM questions success rate"
    epilog="For support, please contact Adi."

    def __init__(self):
        self.arg_parser = ArgumentParser(prog=self.prog, description=self.description, epilog=self.epilog)
        self.arg_parser.add_argument("-c", "--count-questions", type=int, default=50, help="Amount of random qestions to ask")
        self.arg_parser.add_argument("-q", "--questions-file", type=str, default="train.jsonl", help="Questions file path")
        self.arg_parser.add_argument("-a", "--answers-file", type=str, default="train-labels.lst", help="Answers file path")
    
    def parse_args(self) -> Args:
        return self.arg_parser.parse_args()
