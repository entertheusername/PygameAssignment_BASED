# This file is for question generation logic
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
from BackEnd.GameEngine_question import Question

class Generator:
    def __init__(self):
        self.BASES = [2, 8, 10, 16]

    def generate_mixed_calculation(self) -> Question:
        """
        Generate either addition, subtraction or conversion question.
        :return: Question random choice
        """
        return random.choice([self.generate_addition(), self.generate_subtraction(), self.generate_conversion()])
    
    def generate_calculation(self) -> Question:
        """
        Generate either addition or subtraction question.
        :return: Question random choice
        """
        return random.choice([self.generate_addition, self.generate_subtraction])()
    
    def generate_addition(self) -> Question:
        """
        Generate addition question in random base.
        :return: Question addition based
        """
        base = random.choice(self.BASES)
        num1 = random.randint(5, 20)
        num2 = random.randint(5, 20)
        
        str_num1 = self.to_base(num1, base)
        str_num2 = self.to_base(num2, base)
        correct_answer = self.to_base(num1 + num2, base)
        
        return Question(
            f"Add {str_num1} + {str_num2} (base {base})",
            correct_answer,
            "ADDITION",
            base
        )
    
    def generate_subtraction(self) -> Question:
        """
        Generate subtraction question in random base.
        :return: Question subtraction based
        """
        base = random.choice(self.BASES)
        num1 = random.randint(10, 30)
        num2 = random.randint(5, num1 - 1)  # Ensure positive result
        
        str_num1 = self.to_base(num1, base)
        str_num2 = self.to_base(num2, base)
        correct_answer = self.to_base(num1 - num2, base)
        
        return Question(
            f"Subtract {str_num1} - {str_num2} (base {base})",
            correct_answer,
            "SUBTRACTION",
            base
        )

    def generate_conversion(self) -> Question:
        """
        Generate a base conversion question.
        :return: Question conversion based
        """
        source_base, target_base = random.sample(self.BASES, 2)
        decimal_num = random.randint(5, 30)

        # Convert to source base
        source_number = self.to_base(decimal_num, source_base)

        # Calculate correct answer in target base
        decimal_value = int(source_number, source_base)
        correct_answer = self.to_base(decimal_value, target_base)

        question_text = f"Convert {source_number} (base {source_base}) to base {target_base}"
        return Question(question_text, correct_answer, "CONVERSION", target_base)

    def to_base(self, number: int, base: int) -> str:
        """
        Convert number to specified base as string.
        :param number: int normal decimal number
        :param base: int base to convert to
        :return: bin, oct, str, hex converted number
        """
        match base:
            case 2:
                return bin(number)[2:]
            case 8:
                return oct(number)[2:]
            case 10:
                return str(number)
            case 16:  # base 16
                return hex(number)[2:].upper()
