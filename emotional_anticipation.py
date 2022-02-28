from psychopy import visual, core, event
from globals import PsychopyGlobals
from psychopy_questions import QuestionFactory
from util.file_reader import FileReader

from pathlib import Path
from tqdm import tqdm
import csv

import time
import math
import random

class EmotionalAnticipationTask(object):
    def __init__(self, subject_id, task_presentor, conditions=[], num_blocks=1,
                 fixation_time=2, iti_time=6, cue_time=1, movie_time=6.9,
                 num_trials=10, ibi_time=10, variable_isi=False, question_timeouts={},
                 preload_stims=True, practice=False):
        self.task_name = "emotional_anticipation"
        self.subject_id = subject_id

        self.task_presentor = task_presentor

        # From parameter file.
        self.num_blocks = num_blocks
        self.conditions = conditions
        self.fixation_time = fixation_time
        self.iti_time = iti_time
        self.cue_time = cue_time
        self.movie_time = movie_time
        self.num_trials = num_trials
        self.ibi_time = ibi_time
        self.variable_isi = variable_isi
        self.question_timeouts = question_timeouts

        if not practice:
            self.trial_fpath = Path("./resources/emotional_anticipation_trials/")
            self.cue_fpath = Path("./resources/emotional_anticipation_cues/")
            self.video_fpath = Path("./resources/emotional_anticipation_videos/")
        else:
            self.trial_fpath = Path("./resources/emotional_anticipation_trials/practice/")
            self.cue_fpath = Path("./resources/emotional_anticipation_cues/practice/")
            self.video_fpath = Path("./resources/emotional_anticipation_videos/practice/")
            self.num_trials=8
            self.num_blocks=1
        self.practice = practice


        # this is used for testing purposes only.
        if preload_stims:
            self.stim_dictionary = self.create_stim_dictionary(shuffle=practice)

        # Keeping track of state
        self._block_num=0
        self.trials_presented = 0

        self.instructions = self.task_presentor.read_instructions_from_file(self.task_name)
        self.question_factory = QuestionFactory(self.task_presentor,
                                                mode="likert",
                                                snap_for_all=True)

        # Timers
        self.cue_timer = core.CountdownTimer(self.cue_time)
        self.question_timer = core.CountdownTimer(self.question_timeouts["slider affect"])
        self.movie_timer = core.CountdownTimer(self.movie_time)


    def set_current_block_num(self, block_num):
        self._block_num = block_num


    def create_cue_stim(self, cue_tag):

        return visual.ImageStim(self.task_presentor.window,
                                name=f"cue_{cue_tag}",
                                image=f"{self.cue_fpath}/{cue_tag}.png",
                                size=(0.2, 0.3))


    def create_video_stim(self, video_name):

        if video_name == "None":
            return None
        return visual.MovieStim3(win=self.task_presentor.window,
                                 filename=f"{self.video_fpath}/{video_name}", 
                                 noAudio=True)


    def create_stim_dictionary(self, shuffle=False):

        lines = FileReader(f"{self.trial_fpath}/emotional_anticipation_trials.csv").return_rows()

        lines = lines[1:]

        if shuffle:
            random.shuffle(lines)

        stim_dictionary = {}
        for l in tqdm(lines[1:], desc="Loading Stims"):
            cue = self.create_cue_stim(l[0])
            video = self.create_video_stim(l[2])

            if video != None:
                key = l[2]
            else:
                key = f"{l[0]}_None"

            stim_dictionary[key] = {"cue": cue, "video": video, "affect_level": l[3], "video_time": l[4]}

        return stim_dictionary


    def run_full_task(self, practice=False):

        self.task_presentor.display_experimenter_wait_screen("experimenter")
        self.task_presentor.display_instructions(self.instructions)
        self.task_presentor.draw_wait_for_scanner()

        for block in range(self.num_blocks):
            self.set_current_block_num(block)
            self.run_block(block_num=block)
            if (self.num_blocks > 1 and not self.practice):
                self.task_presentor.run_ibi(self.ibi_time)


    def run_block(self, block_num=0, condition="darker"):

        self.task_presentor.trigger_handler.send_string_trigger("Emotional_Anticipation_Block_Start")

        for trial, trial_data in self.stim_dictionary.items():
            if self.trials_presented < self.num_trials:
                self.run_single_trial(trial_data)
                self.task_presentor.run_isi(self.iti_time)
                self.trials_presented += 1
                print(self.trials_presented)
                print(self.num_trials)

        self.task_presentor.trigger_handler.send_string_trigger("Emotional_Anticipation_Block_End")


    def run_single_trial(self, trial_data, has_video=False):

        # Trigger
        cue_time, cue_off_time = self.display_cue(trial_data["cue"])
        self.task_presentor.run_isi(self.fixation_time)
        if trial_data["video"] != None:
            video_start_time, video_end_time = self.display_video(trial_data["video"])
            has_video = True
        else:
            video_start_time = time.time()
            self.task_presentor.run_isi(self.fixation_time)
            video_end_time = time.time()
            has_video = False

        affect_data = self.run_affect_prompt(had_video=has_video)
        print(affect_data)
        self.write_data(trial_data["cue"].name, cue_time, cue_off_time,
                        video_start_time, video_end_time, affect_data[-3], 
                        affect_data[-2], affect_data[-1])


    def display_cue(self, cue):

        cue_time = time.time()
        self.task_presentor.trigger_handler.send_string_trigger("Emotional_Anticipation_Cue_Displayed")
        self.task_presentor.display_stim(cue)
        self.cue_timer.reset()
        while self.cue_timer.getTime() > 0:
            continue
        cue_off_time = time.time()

        self.task_presentor.trigger_handler.send_string_trigger("Emotional_Anticipation_Cue_Removed")
        return (cue_time, cue_off_time)


    def display_video(self, movie_stim):

        start_t = time.time()
        self.movie_timer.reset()
        self.task_presentor.trigger_handler.send_string_trigger("Emotional_Anticipation_Video_Displayed")

        while self.movie_timer.getTime() > 0:
            self.task_presentor.display_stim(movie_stim)

        self.task_presentor.trigger_handler.send_string_trigger("Emotional_Anticipation_Video_End")
        return (start_t, time.time())


    def run_affect_prompt(self, had_video=False):

        ### Has video flag should change the text for the question (will update in question factory).
        self.question_timer.reset()
        self.question_factory.create_question("emotional_SAM")
        self.question_factory.display_question_button_slider(self.question_timer)
        return self.question_factory.get_data_line(self.subject_id, self._block_num)

        # self.task_presentor.logger.write_data_row(self.question_factory.get_data_line(self.subject_id, self._block_num))


    def write_data(self, cue, cue_time, cue_off_time, video_start_time, video_end_time,
                   affect_data_score, affect_data_onset, affect_data_dur):

        data = [self.subject_id,
                cue_time,
                cue_off_time,
                cue_off_time - cue_time,
                cue,
                self._block_num,
                "Video",
                video_start_time,
                video_end_time,
                video_end_time - video_start_time,
                affect_data_score,
                affect_data_onset,
                affect_data_dur]

        self.task_presentor.logger.write_data_row(data)
