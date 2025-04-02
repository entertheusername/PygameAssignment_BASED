# This file is for question logic

class Question:
    __slots__ = ['question_text', 'correct_answer', 'question_type', 'base']

    def __init__(self, question_text: str, correct_answer: str, question_type: str, base: int):
        self.question_text = question_text
        self.correct_answer = correct_answer
        self.question_type = question_type
        self.base = base

