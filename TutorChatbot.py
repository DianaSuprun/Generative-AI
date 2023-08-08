import time
from Fine_Tuning import fine_tuned_model_name
import openai
from Constants import ANSWERING,CHECKING_ANSWERS,CLARIFICAION,RE_EXPLAINING,REQUEST_CLARIFICATION,INITIAL_PROMPT,PRAISE,SET_TASK,SET_UP,SAY_BAY


# Creating full algorithm of communication
class TutorChatbot:

    # Initialize the TutorChatbot with the given probabilities
    def __init__(self):
        self.conversation_history = []
        self.mistakes = []
        self.attempts = 6
        self.current_theme_number = 0

    # Function that counts how much it passed before the last question
    def timeout_decorator(self, timeout_minutes):
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                elapsed_time = time.time() - start_time
                if elapsed_time > timeout_minutes * 60:
                    print(f"Function '{func.__name__}' took more than {timeout_minutes} minutes.")
                    respose_tokens = self.clarifiing()
                    return self.algoritgm_responses('yes', 'no', respose_tokens)
                return result
            return wrapper
        return decorator

        # Function to communicate with fine-tuned Chat GPT
        @timeout_decorator(3)
        def communicate_with_gpt(self, question, user_text):
            conversation = self.conversation_history + [{"role": "system", "content": question},
                                                        {"role": "user", "content": user_text}]
            response = openai.Completion.create(
                engine=fine_tuned_model_name,
                messages=[
                    {"role": "system", "content": question},
                    {"role": "user", "content": user_text}],
                # Use the fine-tuned model for responses
                prompt="\n".join(conversation),
                max_tokens=150,
                temperature=0.7,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None,
            )
            return response['choices'][0]['text'].strip()

        # Ending the conversation
        def end_with_gpt(self, question, user_text):
            conversation = self.conversation_history + [{"role": "system", "content": question},
                                                        {"role": "user", "content": user_text}]
            response = openai.Completion.create(
                engine=fine_tuned_model_name,
                messages=[
                    {"role": "system", "content": question},
                    {"role": "user", "content": user_text}],
                prompt="\n".join(conversation),
                max_tokens=150,
                temperature=0.7,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None,
            )
            return response['choices'][0]['text'].strip()

        # Function to start a communication with fine-tuned Chat GPT
        # 1 step: Chat GPT stars a conversation
        def start_conversation(self, theme):
            current_theme = theme
            initial_prompt = SET_UP + f'{current_theme}' + INITIAL_PROMPT
            chat_gpt_response = self.communicate_with_gpt(initial_prompt, "")
            self.conversation_history.append("Virtual Tutor: " + chat_gpt_response)

        # 2 step: clarifying if everything was understandable
        def clarifiing(self):
            question = CLARIFICAION
            chat_gpt_response = self.communicate_with_gpt(question,'')
            self.conversation_history.append("Virtual Tutor: " + chat_gpt_response)
            user_text = input("Child: ")
            response_tokens = user_text.split()
            self.conversation_history.append("Child: " + user_text)
            return response_tokens

        # 3 step: work with answers. May use in another function
        def algoritgm_responses(self, positive_word, negative_word, response_tokens):
            if positive_word in response_tokens:  # "yes"
                question = PRAISE
                chat_gpt_response = self.communicate_with_gpt(question, '')
                self.conversation_history.append("Virtual Tutor: " + chat_gpt_response)
            if negative_word in response_tokens:  # "no"
                for attempt in range(1, self.attempts + 1):
                    question = REQUEST_CLARIFICATION
                    chat_gpt_response = self.communicate_with_gpt(question, "")
                    self.conversation_history.append("Virtual Tutor: " + chat_gpt_response)
                    user_text = input("Child: ")
                    self.mistakes.append("Child: " + user_text)
                    self.conversation_history.append("Child: " + user_text)
                    question = RE_EXPLAINING
                    chat_gpt_response = self.communicate_with_gpt(question, user_text)
                    self.conversation_history.append("Virtual Tutor: " + chat_gpt_response)
            else:
                question = ANSWERING
                user_text = input("Child: ")
                self.conversation_history.append("Child: " + user_text)
                chat_gpt_response = self.communicate_with_gpt(question, user_text)
                self.conversation_history.append("Virtual Tutor: " + chat_gpt_response)

        # 3 step: check the info
        def asking_task(self, num, level):
            number_of_question = num
            level_of_question = level
            self.attempts = 2
            for i in range(1, number_of_question + 1):  # limit on the number of explanations
                question = "Provide a math task accourding to the disscused theme on the" + f'{level_of_question}' + SET_TASK
                chat_gpt_response = self.communicate_with_gpt(question, "")
                self.conversation_history.append("Virtual Tutor: " + chat_gpt_response)
                user_text = input("Child: ")
                self.conversation_history.append("Child: " + user_text)
                question = "You were given answer to previous task. to the previous task:"+ f"{self.conversation_history[-1]}"+ CHECKING_ANSWERS
                response_token = self.communicate_with_gpt(question, user_text)
                self.conversation_history.append("Virtual Tutor: " + response_token)
                try:
                    if response_token == 'uncorrect':
                        for attempt in range(1, self.attempts + 1):  # limit on the number of explanations
                            question = REQUEST_CLARIFICATION
                            chat_gpt_response = self.communicate_with_gpt(question, '')
                            self.conversation_history.append("Virtual Tutor: " + chat_gpt_response)
                            user_text = input("Child: ")
                            self.conversation_history.append("Child: " + user_text)
                            question = ANSWERING
                            chat_gpt_response = self.communicate_with_gpt(question, user_text)
                            self.conversation_history.append("Virtual Tutor: " + chat_gpt_response)
                            response = self.algoritgm_responses("yes", 'no', user_text)
                except:
                    pass

        # 3 step: moving to the next topic
        def move_to_next_task(self):
            question = PRAISE
            return self.communicate_with_gpt(question,"")

        def end_conversation(self):
            question = SAY_BAY
            return self.end_with_gpt(question, "")

        def order(self, theme, number_of_questions, level_of_questions):
            for i in range(len(theme)):
                if i < len(theme):
                    self.current_theme_number = theme.get(i)
                    self.start_conversation(self.current_theme_number)
                    self.clarifiing()
                    self.asking_task(number_of_questions, level_of_questions)
                    self.move_to_next_task()
                if i == len(theme):
                    self.current_theme_number = theme.get(i)
                    self.start_conversation(self.current_theme_number)
                    self.clarifiing()
                    self.asking_task(number_of_questions, level_of_questions)
                    self.end_conversation()