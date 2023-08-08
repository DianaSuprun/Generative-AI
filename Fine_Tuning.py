import openai
import pandas as pd

# 1 step: preparing functions
# For example I'll use CIMA tutoring dataset. As authors said it has such structure in JSON fornat file
# Tutor Action Key: [Question, Hint/Information Reveal, Correction, Confirmation, Other]
# Student Action Key: [Guess, Question, Affirmation, Other]


#fine-tuninf  GPT-3 model
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

# 4 step: combining
fine_tuned_model_name = "cima_tutiring"
dialog_id = create_fine_tuned_model(train_file_path, base_model="curie", fine_tuned_model_name=fine_tuned_model_name)

follow_fine_tuning_progress(dialog_id)