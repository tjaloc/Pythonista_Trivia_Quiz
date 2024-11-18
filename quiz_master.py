
class QuizMaster:
  def __init__(self, questions: list):
    self.question_nr = 0
    self.questions = questions
    self.current_question = None

  def check_answer(self, user_answer: str) -> bool:
    answer = self.current_question.answer
    return user_answer == answer

  def next_question(self):
    '''Pulls question from question_list depending on current question_number. And return True if answer is correct resp. False for wrong answer.'''
    self.current_question = self.questions[self.question_nr]
    self.question_nr += 1

    return {
      'Nr': f"Question {self.question_nr}",
      'Category': f"{self.current_question.category}",
      'Question': f"\n\n{self.current_question.text}",
      }

  def questions_left(self):
    '''Return True if there are still questions left.'''
    return self.question_nr <= len(self.questions) - 1

