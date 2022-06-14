from psychopy import visual, core
from psychopy_questions import QuestionFactory
from util.file_reader import FileReader
from input_handler import InputHandler

from pathlib import Path
from tqdm import tqdm

import time
import random

class EpisodicProspectionTask(object):
    def __init__(self, subject_id, task_presentor, conditions=[], num_blocks=1, cue_time=15,
                 fixation_time=2, iti_time=6, num_trials=10, ibi_time=10, question_timeouts={},
                 variable_isi=False, practice=False):
        self.task_name = "episodic_prospection"
        self.subject_id = subject_id

        if not practice:
            self.trial_fpath = Path("./resources/episodic_prospection_trials/")
        else:
            self.trial_fpath = Path("./resources/episodic_prospection_trials/practice/")

        self.task_presentor = task_presentor
        self.instructions = self.task_presentor.read_instructions_from_file(self.task_name)

        self.num_blocks = num_blocks
        self.conditions = conditions
        self.fixation_time = fixation_time
        self.iti_time = iti_time
        self.num_trials = num_trials
        self.ibi_time = ibi_time
        self.variable_isi = variable_isi
        self.question_timeouts = question_timeouts

        self.text_size_mult = 1.2

        self.trials = self.parse_trial_data(shuffle=True)

        self.question_factory = QuestionFactory(self.task_presentor,
                                        mode="likert",
                                        snap_for_all=True)

        self.trial_timer = core.CountdownTimer(cue_time)
        self.question_timer = core.CountdownTimer(self.question_timeouts["slider affect"])
        self.input_handler = InputHandler()

        self.condition_stims = {
            "0": visual.TextStim(self.task_presentor.window, text="Zukünftiges Ereignis", pos=(0.0, 0.5), height=(0.1*self.text_size_mult)),
            "1": visual.TextStim(self.task_presentor.window, text="Satz bilden", pos=(0.0, 0.5), height=(0.1*self.text_size_mult))
        }


    def create_word_stim(self, string):

        return visual.TextStim(self.task_presentor.window, text=string, pos=(0.0, 0.0), height=(0.1*self.text_size_mult))



    def parse_trial_data(self, shuffle=False):

        lines = FileReader(f"{self.trial_fpath}/episodic_prospection_trials.csv").return_rows()
        lines = lines[1:]

        if shuffle:
            random.shuffle(lines)

        stim_dictionary = {}
        for l in tqdm(lines, desc="Loading Stims"):
            word = self.create_word_stim(l[0])
            stim_dictionary[l[0]] = {"stim": word,
                                    "word": l[0], 
                                    "valence_level": l[1],
                                    "arousal_level": l[2],
                                    "conreteness_level": l[3],
                                    "frequency": l[4],
                                    "imageability": l[5],
                                    "condition": l[6]}

        return stim_dictionary


    def run_full_task(self):

        self.task_presentor.display_experimenter_wait_screen("experimenter")
        self.task_presentor.display_instructions(self.instructions)
        self.task_presentor.draw_wait_for_scanner()
        self.scan_start = time.time()

        for block in range(self.num_blocks):
            self.run_block(block_num=block)


    def run_block(self, block_num=0):

        self.task_presentor.trigger_handler.send_string_trigger("Episodic_Prospection_Block_Start")
        count = 0
        for trial in self.trials.values():
            self.run_single_trial(trial)
            count += 1
            if count == 14 or count == 28:
                self.display_break()
        self.task_presentor.trigger_handler.send_string_trigger("Episodic_Prospection_Block_End")


    def display_break(self):

        self.task_presentor.trigger_handler.send_string_trigger("Episodic_Prospection_Block_End")
        self.task_presentor.run_isi(30, instead_focus="Sie haben nun eine kurze Pause von 30 Sekunden")
        self.task_presentor.trigger_handler.send_string_trigger("Episodic_Prospection_Block_Start")


    def run_single_trial(self, trial_data, block_num=0):

        export_row = {}

        # self.task_presentor.run_isi(self.task_presentor.sample_variable_isi(6, 1))
        self.task_presentor.run_isi(self.iti_time)
        self.task_presentor.display_stims([trial_data["stim"], self.condition_stims[trial_data["condition"]]])

        self.trial_timer.reset()
        inp = self.input_handler.handle_button_input("default", timer=self.trial_timer)
        if inp:
            export_row["time_pressed"] = time.time()
            export_row["is_button_pressed"] = 1
            while self.trial_timer.getTime() > 0:
                continue
        else:
            export_row["time_pressed"] = None
            export_row["is_button_pressed"] = 0

        self.question_factory.create_question("wie_detalliert")
        self.question_timer.reset()
        question_presented = time.time()
        self.question_factory.display_question_button_slider(self.question_timer, speed_dampen=0.5)
        question_responsed = time.time()
        q_data = self.question_factory.get_data_line(self.subject_id, block_num)
        self.write_data(trial_data["word"], export_row, q_data, question_presented, question_responsed)


    def write_data(self, word, row, q_data, question_presented, question_responsed):

        for elm in q_data:
            print(elm)

        data = [self.subject_id,
                time.time(),
                word,
                0,
                row["time_pressed"],
                row["is_button_pressed"],
                q_data[-6],
                question_presented,
                question_responsed,
                q_data[-1],
                self.scan_start]

        self.task_presentor.logger.write_data_row(data)
