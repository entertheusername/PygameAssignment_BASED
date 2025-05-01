# Import modules
import random

# Allow parent directory to system paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BackEnd.Question_generator import Generator, Question

class AnswerGenerator:
    """
    Create answers matches with the questions and their bases. (30 offset)
    """
    def __init__(self, gamemode: str):
        """
        Initialise the answer object.
        
        :param gamemode: A string representing the selected gamemode.
        """
        self.base_generator = Generator()
        self.gamemode = gamemode

    def generate_question_data(self) -> tuple[Question | None, list[str]]:
        """
        Generates a question object and derives wrong answers from it.

        :returns: A tuple containing question_text, correct_answer and a list of wrong_answers.
        """
        question_obj: Question | None = self.base_generator.generate_question(self.gamemode)

        if not question_obj:
            print ("Error generating question.")
            return None, []
        
        wrong_answers = self.generate_wrong_answers(question_obj, num_wrong=20)
        return question_obj, wrong_answers

    def generate_wrong_answers(self, question: Question, num_wrong: int) -> list[str]:
        """
        Generates a list of unique wrong answers related to the given question.
        
        :param question: A question object containing the correct answer and its base.
        :param num_wrong: The number of wrong answers to generate.
        :returns: A list of unique wrong answers.
        """
        wrong_answers_set = set()
        attempts = 0
        max_total_attempts = num_wrong * 30 # Limit overall attempts
        correct_answer = str(question.correct_answer)
        target_base = question.target_base

        while len(wrong_answers_set) < num_wrong and attempts < max_total_attempts:
            attempts += 1
            # Generate a potential wrong answer using the Question's context (base, correct value)
            offset = random.randint(-15, 15)
            if offset == 0: 
                continue

            try:
                decimal_correct = int(correct_answer, target_base)
            except ValueError:
                print(f"Error converting correct answer '{correct_answer}' with base {target_base}")
                continue # Skip this attempt

            wrong_decimal = decimal_correct + offset
            # Handle negatives
            if wrong_decimal < 0:
                wrong_decimal = abs(wrong_decimal)

            # Convert back to the required base using the helper from the base generator
            wrong_answer = self.base_generator.to_base(wrong_decimal, target_base)

            # Add to set if it's unique and not the correct answer
            if wrong_answer != correct_answer and wrong_answer not in wrong_answers_set:
                wrong_answers_set.add(wrong_answer)

        return list(wrong_answers_set)
