import csv
import datetime
import os

class DataLogger(object):
    def __init__(self, subject_id, task_name):
        self.root_data_dir = "./data/"
        self.subject_id = subject_id
        self.task_name = task_name
        self.current_time = str(datetime.datetime.now())
        # So windows doesn't cry.
        for sep in [":", " ", "."]:
            self.current_time = self.current_time.replace(sep, "_")


    def set_current_task(self, task):
        self.task_name = task
        self.create_export_file()


    def create_export_file(self):

        if not os.path.exists(f"{self.root_data_dir}{self.task_name}"):
            os.mkdir(f"{self.root_data_dir}{self.task_name}")

        with open(f"{self.root_data_dir}{self.task_name}/{self.subject_id}_{self.task_name}_{self.current_time}.csv", "w") as out_csv:
            writer = csv.writer(out_csv, delimiter=",")

            writer.writerow(self.get_data_header())


    def write_data_row(self, data_row):

        assert len(data_row) == len(self.get_data_header())

        with open(f"{self.root_data_dir}{self.task_name}/{self.subject_id}_{self.task_name}_{self.current_time}.csv", "a") as out_csv:
            writer = csv.writer(out_csv, delimiter=",")

            writer.writerow(data_row)


    def get_data_header(self):

        if self.task_name == "affect_reading":
            return ["subject_id",
                    "timestamp",
                    "response_time",
                    "block_num",
                    "question_type",
                    "question_text",
                    "response_numbers",
                    "response_strings",
                    "response_value",
                    "response_string",
                    "is_correct",]
                    # Pass data of previous page reading time into multiple choice question.
        elif self.task_name == "stroop":
            return ["subject_id",
                    "timestamp",
                    "block_num",
                    "trial_num",
                    "display_text",
                    "display_color",
                    "trial_type",
                    "response_accuracy",
                    "response_time"]
        elif self.task_name == "finger_tapping":
            return ["subject_id",
                    "timestamp",
                    "block_num",
                    "hand_condition",
                    "bpm",
                    "event"]
