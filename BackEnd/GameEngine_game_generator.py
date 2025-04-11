# This file is for generating questions and apples
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
from BackEnd.GameEngine_apple import Apple
from BackEnd.GameEngine_question_generator import Generator
from BackEnd.GameEngine_constants import *


class GameGenerator:
    def __init__(self, game, gamemode):
        self.game = game
        self.generator = Generator()
        self.question = None
        match gamemode:
            case "conversion":
                self.question_generator = self.generator.generate_conversion
            case "calculation":
                self.question_generator = self.generator.generate_calculation
            case "mixed_calculation":
                self.question_generator = self.generator.generate_mixed_calculation

    def generate_question(self):
        self.question = self.question_generator()
        return self.question.question_text, self.generate_apples()

    def generate_apples(self):
        apples = []

        correct_pos = random.randint(0, 2)  # Random position for correct answer (0-2)
        positions = []  # Track x positions to prevent overlap
        answers = {self.question.correct_answer}

        for i in range(3):
            is_correct = (i == correct_pos)

            # Use correct answer for correct apple, generate wrong answer otherwise
            if is_correct:
                value = self.question.correct_answer
            else:
                value = self.generate_wrong_answer(answers)
                answers.add(value)

                print(value)
                print(answers)

            x = self.get_valid_x_position(positions)
            positions.append(x)
            y = random.randint(1, 30)
            apples.append(Apple(self.game, x, y, value, is_correct))

        return apples

    def generate_wrong_answer(self, existing_wrong_answer):
        # Generating wrong answer 
        while True:
            value = random.randint(-10, 10)
            if value == 0:
                continue

            decimal_correct_answer = int(self.question.correct_answer, self.question.base)
            wrong_answer = decimal_correct_answer + value

            if wrong_answer < 0:
                wrong_answer = abs(wrong_answer)

            based_wrong_answer = self.generator.to_base(wrong_answer, self.question.base)

            if based_wrong_answer != self.question.correct_answer and based_wrong_answer not in existing_wrong_answer:
                return str(based_wrong_answer)

    def get_valid_x_position(self, existing_positions):
        # Making sure apples do not overlap each other
        while True:
            x = random.randint(APPLE_RADIUS, WIDTH - APPLE_RADIUS)
            # Ensure minimum spacing between apples (2*radius + 20px buffer)
            if all(abs(x - pos) > 2 * APPLE_RADIUS + 30 for pos in existing_positions):
                return x
