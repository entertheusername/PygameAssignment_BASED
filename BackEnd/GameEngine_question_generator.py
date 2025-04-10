import random
from BackEnd.GameEngine_constants import *
from BackEnd.GameEngine_question import Question

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

            op = '+' if question_type == 3 else '-'

            str1, str2 = self.to_base_with_small(num1, base), self.to_base_with_small(num2, base)
            result = num1 + num2 if op == '+' else num1 - num2
            answer = self.to_base(result, base)

            text = f"{'Add' if op == '+' else 'Subtract'} {str1} {op} {str2}"

            return Question(text, answer, "MIXED", base)

        base1, base2 = random.sample(self.BASES, 2)
        target = 10
        num1 = random.randint(5, 30)
        num2 = random.randint(5, 30)

        if question_type == 2 and num1 < num2:
            num1, num2 = num2, num1

        op = '+' if question_type == 1 else '-'
        str1, str2 = self.to_base_with_small(num1, base1), self.to_base_with_small(num2, base2)
        result = num1 + num2 if op == '+' else num1 - num2
        answer = self.to_base(result, target)

        text = f"{'Add' if op == '+' else 'Subtract'} {str1} {op} {str2} and give the answer in  base {target}"

        return Question(text, answer, "MIXED", target)

    def generate_calculation(self) -> Question:
        return random.choice([self.generate_addition, self.generate_subtraction])()

    def generate_addition(self) -> Question:
        base = random.choice(self.BASES)
        num1 = random.randint(5, 20)
        num2 = random.randint(5, 20)

        str_num1, str_num2 = self.to_base_with_small(num1, base), self.to_base_with_small(num2, base)
        correct_answer = self.to_base(num1 + num2, base)

        return Question(f"Add {str_num1} + {str_num2}", correct_answer, "ADDITION", base)

    def generate_subtraction(self) -> Question:
        base = random.choice(self.BASES)
        num1 = random.randint(10, 30)
        num2 = random.randint(5, num1 - 1)

        str_num1, str_num2 = self.to_base_with_small(num1, base), self.to_base_with_small(num2, base)
        correct_answer = self.to_base(num1 - num2, base)

        return Question(f"Subtract {str_num1} - {str_num2}", correct_answer, "SUBTRACTION", base)

    def generate_conversion(self) -> Question:
        source_base, target_base = random.sample(self.BASES, 2)
        decimal_num = random.randint(5, 30)

        source_number = self.to_base(decimal_num, source_base)
        decimal_value = int(source_number, source_base)
        correct_answer = self.to_base(decimal_value, target_base)

        question_text = f"Convert {source_number} base {source_base} to base {target_base}"
        return Question(question_text, correct_answer, "CONVERSION", target_base)

    def to_base(self, number: int, base: int) -> str:
        if base == 2:
            return bin(number)[2:]
        elif base == 8:
            return oct(number)[2:]
        elif base == 10:
            return str(number)
        elif base == 16:
            return hex(number)[2:].upper()
        return str(number)

    def to_base_with_small(self, number: int, base: int) -> str:
        return f"{self.to_base(number, base)} base {base}"

    def render_question_with_base(self, screen, text, center_x, y, font, base_font):
        # Renders a question where numbers with bases display the base in a small rectangle at bottom-right

        words = text.split()
        rendered_parts = []
        skip_next = False

        for i, word in enumerate(words):
            if skip_next:
                skip_next = False
                continue

            if word.lower() == "base" and i > 0 and i < len(words) - 1:
                num_word = words[i - 1]
                base_value = words[i + 1]
                skip_next = True
                rendered_parts.pop()

                num_surface = font.render(num_word, True, Colors.WHITE)
                base_surface = base_font.render(base_value, True, Colors.WHITE)
                rendered_parts.append(("number_with_base", num_surface, base_surface))
            else:
                word_surface = font.render(word, True, Colors.WHITE)
                rendered_parts.append(("word", word_surface))

        # Calculate total width to center it
        padding = 10
        total_width = 0
        for part in rendered_parts:
            if part[0] == "word":
                total_width += part[1].get_width() + padding
            elif part[0] == "number_with_base":
                num_surf, base_surf = part[1], part[2]
                total_width += num_surf.get_width() + base_surf.get_width() + padding // 2

        center_x = (screen.get_width() - total_width) // 2

        for part in rendered_parts:
            if part[0] == "word":
                screen.blit(part[1], (center_x, y))
                center_x += part[1].get_width() + padding

            elif part[0] == "number_with_base":
                num_surface, base_surface = part[1], part[2]
                screen.blit(num_surface, (center_x, y))

                base_x = center_x + num_surface.get_width() - base_surface.get_width() // 2
                base_y = y + num_surface.get_height() - 5  # adjust for alignment
                screen.blit(base_surface, (base_x, base_y))

                center_x += num_surface.get_width() + base_surface.get_width() + padding // 2
