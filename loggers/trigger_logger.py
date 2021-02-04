from loggers.data_logger import DataLogger
import time

class TriggerLogger(DataLogger):
    def __init__(self, subject_id):
        self.subject_id = subject_id
        super().__init__(subject_id, "trigger_data")
        super().create_export_file()

    def write_row(self, row_data):

        row_data.insert(0, self.subject_id)
        super().write_data_row(row_data)
