from psychopy import visual, core, event
from globals import PsychopyGlobals

import time
import math
import datetime
import random

import csv

class StroopTask(object):
    def __init__(self, subject_id, task_presentor, num_blocks=2, fixation_time=2, congruence_rate=.2,
                 num_trials=10, ibi_time=10, variable_isi=True, scoring_method="color_correct", response_timeout=5):
        # scoring methods "congruence" and "color_select"
        self.task_name = "stroop"
        self.subject_id = subject_id
        self.task_presentor = task_presentor
        self.num_blocks = num_blocks
        self.fixation_time = fixation_time
        self.congruence_rate = congruence_rate
        self.num_trials = num_trials
        self.ibi_time = ibi_time
        self.variable_isi = variable_isi
        self.scoring_method = scoring_method
        self.response_timeout = response_timeout
        self.instructions = self.task_presentor.read_instructions_from_file(self.task_name)

        self.response_timer = core.Clock()
        self.trial_timer = core.CountdownTimer(self.response_timeout)

        self._colors = {
                       "red": [(1.0, 0.0, 0.0), "right"],
                       "green": [(0.0, 1.0, 0.0), "down"],
                       "blue": [(0.0, 0.0, 1.0), "left"],
                       }

        # self.export_header = ["subject_id", "timestamp", "block_num", "trial_num",
        #                       "display_text", "display_color", "trial_type",
        #                       "response_accuracy", "response_time"]
        # self.export_lines = [self.export_header, ]


    def run_full_task(self):

        self.task_presentor.display_instructions(self.instructions)

        for block in range(self.num_blocks):
            self.run_block(block_num=block)
            self.task_presentor.run_ibi(self.ibi_time)

        # self.export_data()


    def create_congruent_trial(self):

        color = random.choice(["red", "green", "blue"])
        return [visual.TextStim(self.task_presentor.window, text=color, pos=(0.0, 0.0),
                color=self._colors[color][0]),
                self._colors[color][1],
                color,
                color,
                "congruent"]


    def create_incongruent_trial(self):

        color_list = ["red", "green", "blue"]

        # Ensures that the picked color is RANDOM and NOT the same as the Text.
        text = random.choice(color_list)
        color_list.remove(text)
        color = random.choice(color_list)

        return [visual.TextStim(self.task_presentor.window, text=text, pos=(0.0, 0.0),
                color=self._colors[color][0]),
                self._colors[text][1],
                text,
                color,
                "incongruent"]


    def create_trial_list(self):

        num_trials = self.num_trials
        num_congruent = int(math.ceil(num_trials * self.congruence_rate))
        assert num_congruent <= num_trials

        congruent_indexes = random.sample(range(0, num_trials), num_congruent)

        trials = []
        for trial in range(num_trials):
            if trial in congruent_indexes:
                trials.append(self.create_congruent_trial())
            else:
                trials.append(self.create_incongruent_trial())

        return trials


    def run_block(self, block_num=0):

        # create all the trials that will be used.
        trial_list = self.create_trial_list()
        #
        if self.variable_isi:
            isi_list = self.task_presentor.create_variable_isi_list(len(trial_list), self.fixation_time, how="gamma")
            print(isi_list)
        else:
            isi_list = [self.fixation_time for elm in trial_list]

        for indx, trial in enumerate(trial_list):
            self.response_timer.reset()
            self.trial_timer.reset()
            self.task_presentor.display_stim(trial[0])

            key = event.waitKeys(keyList=['right', 'down', 'left'])

            rt = self.response_timer.getTime()

            if key[0] == trial[1]:
                response = "correct"
            else:
                response = "incorrect"


            self.task_presentor.logger.write_data_row([self.subject_id,
                                                       time.time(),
                                                       block_num,
                                                       indx,
                                                       trial[2],
                                                       trial[3],
                                                       trial[4],
                                                       response,
                                                       rt * 1000])

            # Run ITI
            self.task_presentor.run_isi(isi_list[indx])


    # def export_data(self):
    #
    #     now = datetime.datetime.now()
    #     with open(f"./data/{self.subject_id}_{now.year}_{now.month}_{now.day}", "w") as out_csv:
    #         writer = csv.writer(out_csv, delimiter=",")
    #
    #         for row in self.export_lines:
    #             writer.writerow(row)
