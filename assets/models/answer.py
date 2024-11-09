from assets.models.question import Question

class Answer:
    question: Question
    answer_text: str

    def __init__(self, question: Question):
        self.question = question