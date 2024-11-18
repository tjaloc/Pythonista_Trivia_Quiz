"""fetch trivia questions from the open trivia database api
docs: 
  https://opentdb.com/api_config.php
  
example url:
  https://opentdb.com/api.php?amount=10&category=9&type=boolean
  
json response:
    [{
        'category': 'Entertainment: Japanese ...', 
        'type': 'boolean', 
        'difficulty': 'easy', #'medium' or 'hard'
        'question': 'In the 1988 film ...', 
        'correct_answer': 'True', 
        'incorrect_answers': ['False']
    },...]
"""
import requests
import pprint


categories = {
  9: 'General Knowledge',
  10: 'Books',
  11: 'Film',
  12: 'Music',
  13: 'Musicals & Theatres',
  14: 'Television',
  15: 'Video Games',
  16: 'Board Games',
  17: 'Science & Nature',
  18: 'Computers',
  19: 'Mathematics',
  20: 'Mythology',
  21: 'Sports',
  22: 'Geography',
  23: 'History',
  24: 'Politics',
  25: 'Art',
  26: 'Celebrities',
  27: 'Animals',
  28: 'Vehicles',
  29: 'Comics',
  30: 'Gadgets',
  31: 'Anime & Manga',
  32: 'Cartoons & Animation',
}

class API_Request():
  def __init__(self, questions, category):
    self.retry = 0
    self.endpoint = 'http://opentdb.com/api.php'
    self.params = {
        'amount': questions,
        'category': category,
        #'difficulty': 'easy',
        'type': 'boolean',
    }
    
  def fetch_data(self):
    response = requests.get(
      self.endpoint, 
      params=self.params, 
      timeout=2,
      )
    if response.status_code == 200:
      self.data = response.json()['results']
      
      # sometimes an empty json is returned
      # seemingly because there aren't enough True/False questions in the chosen category
      if not self.data and self.retry < 3:
        self.retry += 1
        self.fetch_data()
        
      return self.data
    else:
      return False
    
if __name__ == '__main__':
  data = API_Request(5, None).fetch_data()
  pprint.pprint(data, width=46)
