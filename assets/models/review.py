from assets.models.answer import Answer

class Review:
    answer: Answer

    def to_answer() -> Answer:
        return