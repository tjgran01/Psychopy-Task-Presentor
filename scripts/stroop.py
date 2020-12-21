from psychopy import visual, core, event
from globals import StroopGlobals

import time
import datetime
import random

import csv

class StroopTask(object):
    def __init__(self, subject_id, num_blocks=2, fixation_time=2, congruence_rate=.2, num_trials=10, ibi_time=10):
        self.subject_id = subject_id
        self.num_blocks = num_blocks
        self.fixation_time = fixation_time
        self.congruence_rate = congruence_rate
        self.num_trials = num_trials
        self.ibi_time = ibi_time

        self.globals = StroopGlobals()
        self.window = self.globals.window
        self.display_drawer = self.globals.the_drawer
        self.instr = self.globals.instructions
        self.advance_text = visual.TextStim(self.window, text="Press 'SPACEBAR' to advance to the next page.",
                                            colorSpace='rgb', color=(1.0, 0.0, 0.0), pos=(0.0, -0.8))
        self.fixation_cross = visual.TextStim(self.window, text="+")
        self.response_timer = core.Clock()
        self._colors = {
                       "red": [(1.0, 0.0, 0.0), "right"],
                       "green": [(0.0, 1.0, 0.0), "down"],
                       "blue": [(0.0, 0.0, 1.0), "left"],
                       }

        self.export_header = ["subject_id", "timestamp", "block_num", "trial_num", "display_text", "display_color", "trial_type", "response_accuracy", "response_time"]
        self.export_lines = [self.export_header, ]

        self.display_instructions()

        for block in range(self.num_blocks):
            self.run_block(block_num=block)
            self.run_ibi()

        self.export_data()


    def run_ibi(self):

        self.display_drawer.add_to_draw_list(self.fixation_cross)
        self.display_drawer.draw_all()
        self.window.flip()
        core.wait(self.ibi_time)

    def display_instructions(self):

        for text_prompt in self.instr:
            display_text = visual.TextStim(self.window, text=text_prompt)
            self.display_drawer.add_to_draw_list(display_text)
            self.display_drawer.add_to_draw_list(self.advance_text)
            self.display_drawer.draw_all()
            self.window.flip()
            while not event.getKeys(keyList=['space']):
                continue


    def create_congruent_trial(self):

        color = random.choice(["red", "green", "blue"])
        return [visual.TextStim(self.window, text=color, pos=(0.0, 0.0), color=self._colors[color][0]), self._colors[color][1], color, color, "congruent"]


    def create_incongruent_trial(self):

        color_list = ["red", "green", "blue"]
        text = random.choice(color_list)
        color_list.remove(text)
        color = random.choice(color_list)
        return [visual.TextStim(self.window, text=text, pos=(0.0, 0.0), color=self._colors[color][0]), self._colors[text][1], text, color, "incongruent"]



    def create_trial_list(self):

        num_trials = self.num_trials
        num_congruent = round(self.num_trials * self.congruence_rate)

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

        trial_list = self.create_trial_list()

        for indx, trial in enumerate(trial_list):
            self.response_timer.reset()
            self.display_drawer.add_to_draw_list(trial[0])
            self.display_drawer.draw_all()
            self.window.flip()
            # Wait for response.
            key = event.waitKeys(keyList=['right', 'down', 'left'])

            rt = self.response_timer.getTime()
            if key[0] == trial[1]:
                response = "correct"
            else:
                response = "incorrect"

            self.export_lines.append([self.subject_id, time.time(), block_num, indx, trial[2], trial[3], trial[4], response, rt * 1000])

            self.display_drawer.add_to_draw_list(self.fixation_cross)
            self.display_drawer.draw_all()
            self.window.flip()
            core.wait(self.fixation_time)


    def export_data(self):

        now = datetime.datetime.now()
        with open(f"../data/{self.subject_id}_{now.year}_{now.month}_{now.day}", "w") as out_csv:
            writer = csv.writer(out_csv, delimiter=",")

            for row in self.export_lines:
                writer.writerow(row)
