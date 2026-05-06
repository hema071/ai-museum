import json
import os

def save(user_id, messages):

    file_path = f"C:/Users/hemas/OneDrive/Desktop/ai_files/{user_id}.json"

    if os.path.exists(file_path):
        with open(file_path, "w") as file:  # ---------------> diffrent modes like w or x or a
            json.dump(messages, file, indent=4)
            print(f"txt file '{file_path}' was created")

def load(user_id):
    file_path = f"C:/Users/hemas/OneDrive/Desktop/ai_files/{user_id}.json"

    if os.path.exists(file_path):
        with open(file_path, "r") as file:  # ---------------> diffrent modes like w or x or a
            data = json.load(file)
            return data


    return []