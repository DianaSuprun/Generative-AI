from TutorChatbot import TutorChatbot
from TutorPreparation import TutorPreparation

class Order(TutorPreparation, TutorChatbot):
   def __init__(self):
    self.preparation = TutorPreparation()
    self.conversation = TutorChatbot()

   def right_order(self,df):
    theme = self.preparation.inputer_themes()
    number_of_questions =self.preparation.number_of_questions()
    level_of_questions = self.preparation.level_of_questions()
    return self.conversation.order(theme, number_of_questions, level_of_questions)