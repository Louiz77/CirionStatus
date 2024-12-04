from datetime import datetime
import os
from ..config import Config

def logger(message):
    try:
        os.makedirs(Config.LOG_FOLDER, exist_ok=True)

        with open(f"{Config.LOG_FOLDER}/report.log", "a") as my_file:
            my_file.write(f"-{datetime.now()} | {message}\n")

            print("Logger")
    except Exception as e:
        print(e)