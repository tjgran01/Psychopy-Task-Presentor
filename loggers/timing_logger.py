from loggers.data_logger import DataLogger
import time

class TimingLogger(DataLogger):
    def __init__(self, subject_id):
        super().__init__(subject_id, "timing_data")
        super().create_export_file()

    def write_row(self, row_data):

        row_data.insert(1, time.time())
        super().write_data_row(row_data)
