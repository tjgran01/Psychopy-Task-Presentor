from psychopy import visual, core, event
from globals import PsychopyGlobals

import time
import math
import random


class StroopTask(object):
    def __init__(self, subject_id, task_presentor, num_blocks=5,
                 fixation_time=2, congruence_rate_congruent=1.0,
                 congruence_rate_incongruent=.33,
                 num_trials=10, ibi_time=10, variable_isi=True,
                 scoring_method="congruence", response_timeout=5,
                 block_time=0, conditions=[], shuffle_conditions=True):
        # scoring methods "congruence" and "color_select"
        self.task_name = "stroop"
        self.subject_id = subject_id
        self.task_presentor = task_presentor
        self.num_blocks = num_blocks
        self.fixation_time = fixation_time
        self.congruence_rate_congruent = congruence_rate_congruent,
        self.congruence_rate_incongruent = congruence_rate_incongruent,
        self.num_trials = num_trials
        self.ibi_time = ibi_time
        self.variable_isi = variable_isi
        self.scoring_method = scoring_method
        self.response_timeout = response_timeout
        self.instructions = self.task_presentor.read_instructions_from_file(self.task_name)
        self.block_time = block_time
        self.conditions = conditions
        self.shuffle_conditions = shuffle_conditions

        self.text_size_mult = 1.2

        if self.shuffle_conditions:
            random.shuffle(self.conditions)

        self.response_timer = core.Clock()
        self.trial_timer = core.CountdownTimer(self.response_timeout)
        self.block_timer = core.CountdownTimer(self.block_time)

        self._colors = {
                       "red": [(1.0, 0.0, 0.0), "right"],
                       "yellow": [(1.0, 1.0, 0.0), "down"],
                       "blue": [(0.0, 0.0, 1.0), "left"],
                       }


        self.congruent_key_reponses = {"mri": {"congruent": "1",
                                               "incongruent": "2"},
                                       "nirs": {"congruent": "left",
                                                "incongruent": "right"}}

        self.valid_key_responses = {"mri": {"congruence": ["1", "2"],
                                            "color_select": ["1", "2", "3"]},
                                    "nirs": {"congruence": ["right", "left"],
                                             "color_select": ["right", "down", "left"]}}


        # If you are using BLOCK TIME rather than trial number --- generate more trials than you will need (i.e. gen a trial per second).
        if self.block_time != 0:
            self.num_trials = self.block_time


    def run_full_task(self):

        self.task_presentor.display_experimenter_wait_screen("experimenter")

        self.task_presentor.display_instructions(self.instructions)
        self.task_presentor.draw_wait_for_scanner()

        for indx, block in enumerate(self.conditions):
            self.run_block(block_num=indx, condition=block)
            self.task_presentor.run_ibi(self.ibi_time)


    def create_congruent_trial(self):

        color = random.choice(["red", "yellow", "blue"])
        return [visual.TextStim(self.task_presentor.window, text=color, pos=(0.0, 0.0), height=(0.1*self.text_size_mult),
                color=self._colors[color][0]),
                self._colors[color][1],
                color,
                color,
                "congruent"]


    def create_incongruent_trial(self):

        color_list = ["red", "yellow", "blue"]

        # Ensures that the picked color is RANDOM and NOT the same as the Text.
        text = random.choice(color_list)
        color_list.remove(text)
        color = random.choice(color_list)

        return [visual.TextStim(self.task_presentor.window, text=text, pos=(0.0, 0.0), height=(0.1*self.text_size_mult),
                color=self._colors[color][0]),
                self._colors[text][1],
                text,
                color,
                "incongruent"]


    def create_trial_list(self, condition):

        if condition == "congruent":
            self.congruence_rate = self.congruence_rate_congruent[0]
        else:
            self.congruence_rate = self.congruence_rate_incongruent[0]

        num_congruent = int(math.ceil(self.num_trials * self.congruence_rate))
        assert num_congruent <= self.num_trials

        congruent_indexes = random.sample(range(0, self.num_trials), num_congruent)

        trials = []
        for trial in range(self.num_trials):
            if trial in congruent_indexes:
                trials.append(self.create_congruent_trial())
            else:
                trials.append(self.create_incongruent_trial())

        return trials


    def score_trial_response(self, input, answer, trial_type):

        modality = self.task_presentor.present_method

        if self.scoring_method == "color_correct":
            if input == answer:
                return "correct"
            return "incorrect"
        else:
            if trial_type == "congruent":
                if input == self.congruent_key_reponses[modality]["congruent"]:
                    return "correct"
                return "incorrect"
            else:
                if input == self.congruent_key_reponses[modality]["incongruent"]:
                    return "correct"
                return "incorrect"


    def send_response_trigger(self, response):

        if response == "correct":
            self.task_presentor.trigger_handler.send_string_trigger("Stroop_Stim_Response_Correct")
        else:
            self.task_presentor.trigger_handler.send_string_trigger("Stroop_Stim_Response_Incorrect")


    def run_block_of_trials(self, trial_list, isi_list, block_num=0):

        for indx, trial in enumerate(trial_list):
            self.run_single_trial(trial, isi_list[indx], indx, block_num)


    def run_single_trial(self, trial, isi, indx, block_num):

        event.clearEvents()
        self.trial_timer.reset()
        self.response_timer.reset()

        self.task_presentor.trigger_handler.send_string_trigger(f"Stroop_Stim_Displayed_{trial[-1].capitalize()}")
        while self.trial_timer.getTime() > 0:

            if self.block_timer.getTime() == 0:
                block_break = False
            else:
                block_break = True

            self.task_presentor.display_stim(trial[0])


            key = event.getKeys(keyList=self.valid_key_responses[self.task_presentor.present_method][self.scoring_method])

            if key:
                rt = self.response_timer.getTime()

                response = self.score_trial_response(key[0], trial[1], trial[-1])
                self.send_response_trigger(response)


                self.task_presentor.logger.write_data_row([self.subject_id,
                                                       time.time(),
                                                       block_num,
                                                       indx,
                                                       trial[2],
                                                       trial[3],
                                                       trial[4],
                                                       response,
                                                       rt * 1000])

                break

            if block_break and self.block_timer.getTime() < 0:

                response = "Block Timeout"
                self.task_presentor.logger.write_data_row([self.subject_id,
                                                       time.time(),
                                                       block_num,
                                                       indx,
                                                       trial[2],
                                                       trial[3],
                                                       trial[4],
                                                       response,
                                                       -1])
                break


        if self.trial_timer.getTime() < 0:
            self.task_presentor.logger.write_data_row([self.subject_id,
                                                       time.time(),
                                                       block_num,
                                                       indx,
                                                       trial[2],
                                                       trial[3],
                                                       trial[4],
                                                       "TIMEOUT",
                                                       self.response_timeout * 1000])


        # Run ITI
        self.task_presentor.run_isi(isi)


    def run_block(self, block_num=0, condition="incongruent"):

        # create all the trials that will be used.
        self.task_presentor.trigger_handler.send_string_trigger("Stroop_Block_Start")

        trial_list = self.create_trial_list(condition)

        if self.variable_isi:
            isi_list = self.task_presentor.create_variable_isi_list(len(trial_list), self.fixation_time, how="gamma")
        else:
            isi_list = [self.fixation_time for elm in trial_list]

        if self.block_time == 0:
            self.run_block_of_trials(trial_list, isi_list, block_num=block_num)
        else:
            self.block_timer.reset()
            trial_indx = 0
            while(self.block_timer.getTime()) > 0:
                self.run_single_trial(trial_list[trial_indx], isi_list[trial_indx], trial_indx, block_num=block_num)
                trial_indx+=1

        self.task_presentor.trigger_handler.send_string_trigger("Stroop_Block_End")
