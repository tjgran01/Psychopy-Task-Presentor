import pandas as pd

from stroop import StroopTask
from finger_tapping import FingerTappingTask
from affect_reading import AffectReadingTask

import pickle

class TaskFactory(object):
    def __init__(self, sub_id, task_presentor):
        self.sub_id = sub_id
        self.task_presentor = task_presentor


    def try_param_set_from_file(self, task_string):

        try:
            prefs = pd.read_csv(f"./preferences/task_preference_csvs/id_preference_table_{task_string}.csv", dtype={"sub_id": str})
            prefs.set_index("sub_id", inplace=True)
            prefs = prefs.loc[self.sub_id]
            return prefs
        except:
            print(f"WARNING: No preference file found (or preferences file is missing specified Subject ID: {self.sub_id}.)")
            print("Running with Default Arguments")
            return pd.Series()


    def create_task(self, task_string):

        prefs = self.try_param_set_from_file(task_string)
        if prefs.empty:
            return self.create_default_task(task_string)

        if task_string == "stroop":

            task = StroopTask(self.sub_id,
                              self.task_presentor,
                              num_blocks=prefs["num_blocks"],
                              fixation_time=prefs["fixation_time"],
                              congruence_rate=prefs["congruence_rate"],
                              num_trials=prefs["num_trials"],
                              ibi_time=prefs["ibi_time"],
                              variable_isi=prefs["variable_isi"])
        elif task_string == "finger_tapping":

            task = FingerTappingTask(self.sub_id,
                                     self.task_presentor,
                                     num_blocks=prefs["num_blocks"],
                                     block_time=prefs["block_time"],
                                     ibi_time=prefs["ibi_time"],
                                     is_sound=prefs["is_sound"])
        elif task_string == "affect_reading":

            task = AffectReadingTask(self.sub_id,
                                     self.task_presentor,
                                     num_blocks=prefs["num_blocks"],
                                     block_time=prefs["block_time"],
                                     ibi_time=prefs["ibi_time"],
                                     is_sound=prefs["is_sound"])

        return task


    def create_default_task(self, task_string):

        prefs = pickle.load(open(f"./preferences/saved_defaults/{task_string}_defaults.pkl", "rb"))

        print(prefs)

        if task_string == "stroop":

            return StroopTask(self.sub_id, self.task_presentor,
                              num_blocks=prefs["num_blocks"],
                              fixation_time=prefs["fixation_time"],
                              congruence_rate=prefs["congruence_rate"],
                              num_trials=prefs["num_trials"],
                              ibi_time=prefs["ibi_time"],
                              variable_isi=prefs["variable_isi"])
        elif task_string == "finger_tapping":
            return FingerTappingTask(self.sub_id, self.task_presentor,
                                     num_blocks=prefs["num_blocks"],
                                     block_time=prefs["block_time"],
                                     ibi_time=prefs["ibi_time"],
                                     is_sound=prefs["is_sound"])
        elif task_string == "affect_reading":
            return AffectReadingTask(self.sub_id, self.task_presentor,
                                     num_blocks=prefs["num_blocks"],
                                     affect_order=prefs["affect_order"],
                                     max_reading_time=prefs["max_reading_time"],
                                     readings=prefs["readings"],
                                     mult_choice_question_num=prefs["mult_choice_question_num"])
