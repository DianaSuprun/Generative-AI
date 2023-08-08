import openai
import pandas as pd

# 1 step: preparing functions
# For example I'll use CIMa tutoring dataset. As authors said it has such structure in JSON fornat file
# Tutor Action Key: [Question, Hint/Information Reveal, Correction, Confirmation, Other]
# Student Action Key: [Guess, Question, Affirmation, Other]


def prepare_training_data(df, train_file_path):
    with open(train_file_path, "w") as f:
        for index, row in df.iterrows():
            tutor_actions = row["tutorActions"]
            tutor_actions_str = "[" + ", ".join([str(action).lower() for action in tutor_actions]) + "]"
            student_actions = row["studentActions"]
            student_actions_str = "[" + ", ".join([str(action).lower() for action in student_actions]) + "]"
            prompt = row["past_convo"][-2]
            completion = row["past_convo"][-1]
            f.write(
                f'{{"tutor_actions": {tutor_actions_str}, "student_actions": {student_actions_str}, "prompt": "{prompt}", "completion": "{completion}"}}\n')


# 2 step: fine-tuninf  GPT-3 model
def create_fine_tuned_model(train_file_path, base_model="curie", fine_tuned_model_name="cima_tutiring"):
    response = openai.FineTune.create(
        training_file=train_file_path,
        model=base_model,
        fine_tuned_model_name=fine_tuned_model_name
    )
    dialog_id = response['id']
    return dialog_id


def follow_fine_tuning_progress(dialog_id):
    response = openai.FineTune.retrieve(dialog_id)
    while response['status'] == "running":
        print("Fine-tuning in progress. Please wait...")
        response = openai.FineTune.retrieve(dialog_id)
    if response['status'] == "succeeded":
        print(f"Fine-tuned model: {response['fine_tuned_model']}")
    else:
        print("Fine-tuning failed.")


# 3 step: preparing training data in JSON format
df = pd.read_json("cima_dataset.json")  # Replace with needed file path

train_file_path = "cima_dataset_training.json"  # Replace with needed file path
prepare_training_data(df, train_file_path)

# 4 step: combining
fine_tuned_model_name = "cima_tutiring"
dialog_id = create_fine_tuned_model(train_file_path, base_model="curie", fine_tuned_model_name=fine_tuned_model_name)

follow_fine_tuning_progress(dialog_id)