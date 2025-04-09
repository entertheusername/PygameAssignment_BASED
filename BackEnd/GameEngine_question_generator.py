# This file is for question generation logic
import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
from BackEnd.GameEngine_question import Question

class Generator:
    def __init__(self):
        self.BASES = [2, 8, 10, 16]

    def generate_mixed_calculation(self) -> Question:
        
        type = random.choice([1, 2, 3, 4, 5]) # Picking 5 different type of choices
        
        if type == 5:
            return self.generate_conversion() # 5 for conversion
        
        if type in (3, 4): # 3 & 4 for arithmetic logic involving same number bases 
            base = random.choice(self.BASES)
            num1 = random.randint(5, 30)
            num2 = random.randint(5, num1) if type == 4 else random.randint(5, 30)

            if type == 4 and num1 < num2: #Swapping number to make sure subtraction always get positive answer
                num1, num2 = num2, num1 

            op = '+' if type == 3 else '-'

            str1 = self.to_base(num1, base)
            str2 = self.to_base(num2, base)
            result = num1 + num2 if op == '+' else num1 - num2
            answer = self.to_base(result, base)

            text = (f"{'Add' if op == '+' else 'Subtract'} "
                    f"{str1} (base {base}) {op} {str2} (base {base})")


            return Question(text, answer, "MIXED", base)

        base1, base2 = random.sample(self.BASES, 2) 
        target = 10 # Making sure question answer to be number base 10 
        num1 = random.randint(5, 30)
        num2 = random.randint(5, 30)
        
        if type == 2 and num1 < num2:
            num1, num2 = num2, num1 #Swapping number to make sure subtraction always get positive answer
        
        op = '+' if type == 1 else '-'
        str1 = self.to_base(num1, base1)
        str2 = self.to_base(num2, base2)
        result = num1 + num2 if op == '+' else num1 - num2
        answer = self.to_base(result, target)  # Always base 10

        text = (f"{'Add' if op == '+' else 'Subtract'} "
                f"{str1} (base {base1}) {op} {str2} (base {base2}) "
                f"and give the answer in base {target}")

        return Question(text, answer, "MIXED", target)
        
    def generate_calculation(self) -> Question:
        # Generating addition or subtraction
        return random.choice([self.generate_addition, self.generate_subtraction])()
    
    def generate_addition(self) -> Question:
        # Generating addition question using random base

        base = random.choice(self.BASES)
        num1 = random.randint(5, 20)
        num2 = random.randint(5, 20)
        
        str_num1 = self.to_base(num1, base)
        str_num2 = self.to_base(num2, base)
        correct_answer = self.to_base(num1 + num2, base)
        
        return Question(f"Add {str_num1} + {str_num2} (base {self.format_base_subscript(base)})", # To be fixed
               correct_answer, "ADDITION", base)
    
    def generate_subtraction(self) -> Question:
        # Generating subtraction question using random base
        base = random.choice(self.BASES)
        num1 = random.randint(10, 30)
        num2 = random.randint(5, num1 - 1)  # Ensure positive result
        
        str_num1 = self.to_base(num1, base)
        str_num2 = self.to_base(num2, base)
        correct_answer = self.to_base(num1 - num2, base)
        
        return Question(
            f"Subtract {str_num1} - {str_num2} (base {base})", correct_answer, "SUBTRACTION", base)

    def generate_conversion(self) -> Question:
        # Generate a base conversion question

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
        # Converting number to specified base as string
        match base:
            case 2:
                return bin(number)[2:]
            case 8:
                return oct(number)[2:]
            case 10:
                return str(number)
            case 16:  # base 16
                return hex(number)[2:].upper()
