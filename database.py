import json
import os

def save(user_id, messages):

    file_path = f"C:/Users/hemas/OneDrive/Desktop/ai_files/{user_id}.json"
    with open(file_path, "w") as file:  # ---------------> diffrent modes like w or x or a
        json.dump(messages, file, indent=4)
        print(f"txt file '{file_path}' was created")

def load(user_id):
    file_path = f"C:/Users/hemas/OneDrive/Desktop/ai_files/{user_id}"

    if os.path.exists(file_path):
        with open(file_path, "r") as file:  # ---------------> diffrent modes like w or x or a
            print(f"txt file '{file_path}' was read")
            
    return file