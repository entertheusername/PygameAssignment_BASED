import random
import pygame

from BackEnd import Constants

# Question Logic
class Question:
    __slots__ = ['operand1', 'base1', 'operand2', 'base2', 'operator', 'target_base', 'correct_answer', 'question_type']

    def __init__(self, *, operand1: str, base1: int, operand2: str | None, base2: int | None, operator: str, target_base: int, correct_answer: str, question_type: str):
        self.operand1 = operand1
        self.base1 = base1
        self.operand2 = operand2
        self.base2 = base2
        self.operator = operator
        self.target_base = target_base
        self.correct_answer = correct_answer
        self.question_type = question_type

# Generate Questions
class Generator:
    def __init__(self):
        self.BASES = [2, 8, 10, 16]

    def generate_mixed_calculation(self) -> Question:
        question_type = random.choice([1, 2, 3, 4, 5])

        if question_type == 5:
            return self.generate_conversion()

        if question_type in (3, 4):
            base = random.choice(self.BASES)
            num1 = random.randint(5, 30)
            num2 = random.randint(5, num1) if question_type == 4 else random.randint(5, 30)

            if question_type == 4 and num1 < num2:
                num1, num2 = num2, num1

            op_str = '+' if question_type == 3 else '-'
            op1_str = self.to_base(num1, base)
            op2_str = self.to_base(num2, base)
            result_decimal = num1 + num2 if op_str == '+' else num1 - num2
            answer_str = self.to_base(result_decimal, base)

            return Question(operand1=op1_str, base1=base,
                            operand2=op2_str, base2=base,
                            operator=op_str, target_base=base,
                            correct_answer=answer_str, question_type="MIXED_SAME_BASE")

        base1, base2 = random.sample([b for b in self.BASES], 2)
        target_base = 10
        num1 = random.randint(5, 30)
        num2 = random.randint(5, 30)

        if question_type == 2 and num1 < num2: num1, num2 = num2, num1

        op_str = '+' if question_type == 1 else '-'
        op1_str = self.to_base(num1, base1)
        op2_str = self.to_base(num2, base2)
        result_decimal = num1 + num2 if op_str == '+' else num1 - num2
        answer_str = self.to_base(result_decimal, target_base)

        return Question(operand1=op1_str, base1=base1,
                        operand2=op2_str, base2=base2,
                        operator=op_str, target_base=target_base,
                        correct_answer=answer_str, question_type="MIXED_DIFF_BASE")

    def generate_calculation(self) -> Question:
        return random.choice([self.generate_addition, self.generate_subtraction])()

    def generate_addition(self) -> Question:
        base = random.choice(self.BASES)
        num1 = random.randint(5, 20)
        num2 = random.randint(5, 20)
        op1_str = self.to_base(num1, base)
        op2_str = self.to_base(num2, base)
        answer_str = self.to_base(num1 + num2, base)

        return Question(operand1=op1_str, base1=base,
                        operand2=op2_str, base2=base,
                        operator='+', target_base=base,
                        correct_answer=answer_str, question_type="ADDITION")

    def generate_subtraction(self) -> Question:
        base = random.choice(self.BASES)
        num1 = random.randint(10, 30)
        num2 = random.randint(5, num1 - 1)
        op1_str = self.to_base(num1, base)
        op2_str = self.to_base(num2, base)
        answer_str = self.to_base(num1 - num2, base)

        return Question(operand1=op1_str, base1=base,
                        operand2=op2_str, base2=base,
                        operator='-', target_base=base,
                        correct_answer=answer_str, question_type="SUBTRACTION")

    def generate_conversion(self) -> Question:
        source_base, target_base = random.sample(self.BASES, 2)
        decimal_num = random.randint(5, 30)

        source_value = self.to_base(decimal_num, source_base)
        correct_answer = self.to_base(decimal_num, target_base)

        return Question(operand1=source_value, base1=source_base,
                        operand2=None, base2=None,
                        operator='->',
                        target_base=target_base,
                        correct_answer=correct_answer, question_type="CONVERSION")

    def to_base(self, number: int, base: int) -> str:
        if number < 0: 
            number = 0
        if base == 2:
            return bin(number)[2:]
        elif base == 8:
            return oct(number)[2:]
        elif base == 10:
            return str(number)
        elif base == 16:
            return hex(number)[2:].upper()
        return str(number)
