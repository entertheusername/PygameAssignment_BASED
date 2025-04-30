import random
import pygame

from BackEnd import Constants

# Question Logic
class Question:
    __slots__ = ['operand1', 'base1', 'operand2', 'base2', 'operator', 'target_base', 'correct_answer', 'gamemode']

    def __init__(self, *, operand1: str, base1: int, operand2: str | None, base2: int | None, operator: str, target_base: int, correct_answer: str, gamemode: str):
        self.operand1 = operand1
        self.base1 = base1
        self.operand2 = operand2
        self.base2 = base2
        self.operator = operator
        self.target_base = target_base
        self.correct_answer = correct_answer
        self.gamemode = gamemode

    # Helper function skibidi ahhhhhh (To avoid repetition of code in draw_question)
    def render_number_with_base(self, screen, value: str, base: int, x: int, y: int, font: pygame.font.Font, sub_font: pygame.font.Font, color, offset: tuple[int, int]) -> int:
        """
        Renders value and base subscript.
        :param screen:
        :param value:
        :param base:
        :param x:
        :param y:
        :param font:
        :param sub_font:
        :param color:
        :param offset:
        :return:
        """
        offset_x, offset_y = offset
        value_surf = font.render(value, True, color)
        base_surf = sub_font.render(str(base), True, color)
        base_x = x + value_surf.get_width()
        base_y = y + value_surf.get_height() - base_surf.get_height()

        screen.blit(value_surf, (x + offset_x, y + offset_y))
        screen.blit(base_surf, (base_x + offset_x, base_y + offset_y))
        screen.blit(value_surf, (x, y))
        screen.blit(base_surf, (base_x, base_y))

        return value_surf.get_width() + base_surf.get_width()

    def draw_question(self, display, font, sub_font, text_color, bold_offset):
        """
        Render questions with subscript bases
        :param display:
        :param font:
        :param sub_font:
        :param text_color:
        :param bold_offset:
        :return:
        """
        y_pos = 38
        x_padding = 30
        y_padding = 15
        corner_radius = 15
        text_padding = 10
        offset = bold_offset

        total_text_width = 0
        max_text_height = font.get_height() # Base height
        elements_to_render = []

        if self.gamemode == "conversion":
            # Text for conversion
            elements_to_render.append({'type': 'op', 'text': "Convert "})
            elements_to_render.append({'type': 'num', 'value': self.operand1, 'base': self.base1})
            elements_to_render.append({'type': 'op', 'text': f" to base {self.target_base}"})
        else: # Calculation
            elements_to_render.append({'type': 'num', 'value': self.operand1, 'base': self.base1})
            elements_to_render.append({'type': 'op', 'text': f" {self.operator} "})
            if self.operand2 is not None and self.base2 is not None:
                elements_to_render.append({'type': 'num', 'value': self.operand2, 'base': self.base2})
            elements_to_render.append({'type': 'op', 'text': " = ?"})

        # Draw
        for element in elements_to_render:
            width = 0
            if element['type'] == 'num':
                val_surf = font.render(element['value'], True, text_color)
                sub_surf = sub_font.render(str(element['base']), True, text_color)
                width = val_surf.get_width() + sub_surf.get_width()
            else: # op
                op_surf = font.render(element['text'], True, text_color)
                width = op_surf.get_width()
            element['width'] = width
            total_text_width += width
        total_text_width += text_padding * (len(elements_to_render) - 1)

        # Draw semi transparent curved edge rectangle panel (long ahhhh name)
        panel_width = total_text_width + x_padding * 2
        panel_height = max_text_height + y_padding * 2
        panel_x = (Constants.SCREEN_WIDTH - panel_width) // 2
        panel_y = y_pos - y_padding
        panel_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surf.fill((0,0,0,0))
        panel_color = (255,255,255)
        pygame.draw.rect(panel_surf, panel_color, (corner_radius, 0, max(0, panel_width - 2 * corner_radius), panel_height))
        pygame.draw.rect(panel_surf, panel_color, (0, corner_radius, panel_width, max(0, panel_height - 2 * corner_radius)))
        pygame.draw.circle(panel_surf, panel_color, (corner_radius, corner_radius), corner_radius)
        pygame.draw.circle(panel_surf, panel_color, (panel_width - corner_radius, corner_radius), corner_radius)
        pygame.draw.circle(panel_surf, panel_color, (corner_radius, panel_height - corner_radius), corner_radius)
        pygame.draw.circle(panel_surf, panel_color, (panel_width - corner_radius, panel_height - corner_radius), corner_radius)
        panel_surf.set_alpha(100)
        display.blit(panel_surf, (panel_x, panel_y))
        
        # Draw text inside panel
        start_x = panel_x + x_padding
        current_x = start_x
        text_y_pos = panel_y + y_padding

        for i, element in enumerate(elements_to_render):
            element_width = element['width'] 
            if element['type'] == 'num':
                self.render_number_with_base(display, element['value'], element['base'], current_x, text_y_pos, font, sub_font, text_color, offset)
                current_x += element_width + text_padding
            else: # op
                op_surf = font.render(element['text'], True, text_color)
                op_y = text_y_pos + (max_text_height - op_surf.get_height()) // 2
                display.blit(op_surf, (current_x + offset[1], op_y + offset[1]))
                display.blit(op_surf, (current_x, op_y))
                current_x += element_width + text_padding

# Generate Questions
class Generator:
    def __init__(self):
        self.BASES = [2, 8, 10, 16]
        self.GAMEMODES = ["conversion", "basic_calculation", "mixed_calculation"]

    def generate_question(self, gamemode):
        """
        Generate questions for selected gamemode
        :param gamemode:
        :return:
        """
        if gamemode == "conversion":
            return self.generate_conversion()
        elif gamemode == "basic_calculation":
            return self.generate_basic_calculation()
        elif gamemode == "mixed_calculation":
            return self.generate_mixed_calculation()
        else:
            print (f"Error generating question for {gamemode}")

    def generate_conversion(self) -> Question:
        """
        Generate a conversion question from one base to another
        :return:
        """
        source_base, target_base = random.sample(self.BASES, 2)
        decimal_num = random.randint(5, 30)

        source_value = self.to_base(decimal_num, source_base)
        correct_answer = self.to_base(decimal_num, target_base)

        return Question(
            operand1=source_value, 
            base1=source_base,
            operand2=None, 
            base2=None,
            operator='->', 
            target_base=target_base,
            correct_answer=correct_answer, 
            gamemode="conversion"
        )
    
    def generate_basic_calculation(self) -> Question:
        """
        Generate addition or subtraction questions within the same base
        :return:
        """
        operation = random.choice(["ADDITION", "SUBTRACTION"])
        base = random.choice(self.BASES)
        
        if operation == "ADDITION":
            num1 = random.randint(5, 20)
            num2 = random.randint(5, 20)
            op_str = '+'
            result = num1 + num2
        else:  # SUBTRACTION
            num1 = random.randint(10, 30)
            num2 = random.randint(5, num1 - 1)
            op_str = '-'
            result = num1 - num2
            
        op1_str = self.to_base(num1, base)
        op2_str = self.to_base(num2, base)
        answer_str = self.to_base(result, base)

        return Question(
            operand1=op1_str, 
            base1=base,
            operand2=op2_str, 
            base2=base,
            operator=op_str, 
            target_base=base,
            correct_answer=answer_str, 
            gamemode="basic_calculation"
        )
 
    def generate_mixed_calculation(self) -> Question:
        """
        Generate addition or subtraction between different bases
        :return:
        """
        base1, base2 = random.sample(self.BASES, 2)
        target_base = 10  # Answers in decimal

        operation = random.choice(["ADDITION", "SUBTRACTION"])
        
        num1 = random.randint(5, 30)
        num2 = random.randint(5, 30)
        
        # To avoid negative results
        if operation == "SUBTRACTION" and num1 < num2:
            num1, num2 = num2, num1
            
        op_str = '+' if operation == "ADDITION" else '-'
        op1_str = self.to_base(num1, base1)
        op2_str = self.to_base(num2, base2)
        result = num1 + num2 if op_str == '+' else num1 - num2
        answer_str = self.to_base(result, target_base)

        return Question(
            operand1=op1_str, 
            base1=base1,
            operand2=op2_str, 
            base2=base2,
            operator=op_str, 
            target_base=target_base,
            correct_answer=answer_str, 
            gamemode="mixed_calculation"
        )

    def to_base(self, number: int, base: int) -> str:
        """
        Change selected number to base numbers.
        :param number: Decimal number selected.
        :param base: Which base to convert to.
        :return: Base number based on the base given.
        """
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
