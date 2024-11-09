
class Solution:
    """
        A solution model representing a possible solution for a question for the LLM
    """
    solution_text: str
    is_correct: bool

    def __init__(self, solution_text: str, is_correct: bool=False):
        self.solution_text = solution_text
        self.is_correct = is_correct