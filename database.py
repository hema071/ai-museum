import json
import os

folder_path = f"C:/Users/hemas/OneDrive/Desktop/aifiles"

def save(user_id, messages, username, mode):



    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Klasör bulunamadı yeni oluşturuldu: {folder_path}")

    file_path = f"{folder_path}/{user_id}.json"

    data = {
        "username": username,
        "mode": mode,
        "messages": messages
    }

    with open(file_path, "w") as file:  # ---------------> diffrent modes like w or x or a
        json.dump(data, file, indent=4)
        print(f"txt file '{folder_path}' was created")
        print("Dosyanın gerçek konumu:", os.path.abspath(file_path))

def load(user_id):
    file_path = f"{folder_path}/{user_id}.json"

    if os.path.exists(file_path):
        with open(file_path, "r") as file:  # ---------------> diffrent modes like w or x or a
            data = json.load(file)
            return data


    return []