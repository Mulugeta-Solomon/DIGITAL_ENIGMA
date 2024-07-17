import os
import json
from datetime import datetime

class Logger:
    def __init__(self, name):
        self.name = name
        self.green = "\033[32m{}\033[0m"
        self.yellow = "\033[33m{}\033[0m"
        self.blue = "\033[34m{}\033[0m"
        self.basic_red = "\033[31m{}\033[0m"
        self.hard_red = "\033[41m{}\033[0m"
        self.log_file = "../log.json"

        # Ensure the log file exists and is a valid JSON array
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                json.dump([], f)

    def build_time(self):
        date = datetime.now()
        return date.strftime("%d.%m.%Y %H:%M:%S")

    def write_to_log(self, entry):
        try:
            with open(self.log_file, "r+") as f:
                logs = json.load(f)
                logs.append(entry)
                f.seek(0)
                json.dump(logs, f, indent=4)
        except Exception as e:
            print("Failed to write to file", e)

    def log(self, color, *texts):
        message = " ".join(texts)
        entry = {
            "color": color,
            "time": self.build_time(),
            "name": self.name,
            "message": message
        }
        self.write_to_log(entry)
        print(color.format(f"[{self.name}, {self.build_time()}] {message}"))

    def success(self, *texts):
        self.log(self.green, *texts)

    def info(self, *texts):
        self.log(self.yellow, *texts)

    def question(self, *texts):
        self.log(self.blue, *texts)

    def error(self, *texts):
        self.log(self.basic_red, *texts)

    def real_error(self, *texts):
        self.log(self.hard_red, *texts)

# # Example usage:
# logger = Logger("ANNOTATOR")
# logger.success("This is a success message.")
# logger.info("This is an info message.")
# logger.question("This is a question message.")
# logger.error("This is an error message.")
# logger.real_error("This is a real error message.")