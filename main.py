import ui
import html
import sound

from question_model import Question
from quiz_master import QuizMaster
from api_handler import API_Request, categories

WRONG = 'game:Error'
RIGHT = 'arcade:Coin_3'
TAP = '8ve:8ve-tap-simple'
QUESTIONS = 5

class Quizzler:
  def __init__(self):
    self.score = 0
    self.category = None
    self.v = ui.load_view(pyui_path='./bgd.pyui')
    self.content = self.v['content']
    
    self.elements_setup('categories')
    self.v.present('sheet', 'PORTRAIT', hide_title_bar=True)
    
  def parse_category(self, sender):
    _, nr = self.v_categories['category_list'].selected_row
    self.category = nr + 9
    self.new_quiz(None)
    
  def elements_setup(self, view):
    for subview in self.content.subviews:
      self.content.remove_subview(subview)
        
    match view:
      case 'categories':
        self.v_categories = ui.load_view(pyui_path='./categories.pyui')
        self.v_categories['category_list'].data_source = ui.ListDataSource(categories.values())
        self.v_categories.flex ='WH'
        self.v_categories.frame = self.content.bounds
        self.content.add_subview(self.v_categories)
        
      case 'quiz':
        self.v_quiz = ui.load_view(pyui_path='./question.pyui')
        self.v_quiz.frame = self.content.bounds
        self.content.add_subview(self.v_quiz)
    
      case 'end':
        self.v_end = ui.load_view(pyui_path='./end.pyui')
        self.v_end.frame = self.content.bounds
        self.content.add_subview(self.v_end)
      
    self.content.flex = 'WH'
    
  def error_view(self, msg):
    self.v_error = ui.load_view(pyui_path='./error.pyui')
    self.v_error.frame = self.content.bounds
    self.content.add_subview(self.v_error)
        
  def quit(self, sender):
    sound.play_effect('8ve:8ve-slide-network')
    self.v.close()
    
  def delete_text(self):
    for x in ['Nr', 'Category', 'Question', 'score']:
      self.v_quiz[x].text = ''
      
  def new_category(self, sender):
    if sender:
      sound.play_effect(TAP)
    self.elements_setup('categories')
    
  def new_quiz(self, sender):
    sound.play_effect(TAP)
    self.elements_setup('quiz')
    self.score = 0
    self.question_bank = []
    self.delete_text()
    
    trivia = API_Request(QUESTIONS, self.category).fetch_data()
    if not trivia:
      self.error_view("Couldn't fetch questions.")
      
    for question in trivia:
      self.question_bank.append(Question(
        question['question'], 
        question['correct_answer'],
        question['category'])
        )
        
    self.quiz_master = QuizMaster(self.question_bank)
    self.next_question()
    
  def answer_true(self, sender):
    sound.play_effect(TAP)
    is_right = self.quiz_master.check_answer('True')
    self.feedback(is_right)
          
  def answer_false(self, sender):
    sound.play_effect(TAP)
    is_right = self.quiz_master.check_answer('False')
    self.feedback(is_right)
    
  def next_question(self):
    self.v.background_color='#cfd4cd'
    
    if self.quiz_master.questions_left():
      q = self.quiz_master.next_question()
      
      for key, val in q.items():
        self.v_quiz[key].text = html.unescape(val)
  
    else:
        self.elements_setup('end')
        self.delete_text()
        self.v_end['result'].text = f"You've answered {self.score} out of {self.quiz_master.question_nr} questions correctly."
      
  def feedback(self, is_right):
    if is_right:
        # only show score if player has points
        self.score += 1
        if self.score:
          self.v_quiz['score'].text = f'{self.score}'
        
        self.v.background_color='#61ad26'
        sound.play_effect(RIGHT, volume=.5)
    else:
        self.v.background_color='#e1550f'
        sound.play_effect(WRONG, volume=.5)
        
    ui.delay(self.next_question, .5)
    

if __name__ == '__main__':
  Quizzler()
