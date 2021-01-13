import random
from psychopy import visual, core, event

import time
import pandas as pd

from psychopy_questions import QuestionFactory

class AffectReadingTask(object):
    def __init__(self, subject_id, task_presentor, num_blocks=4, affect_order=["happy", "none", "happy", "none"],
                 max_reading_time=180, readings=["hypotheses", "causalclaims", "validity", "variables"],
                 mult_choice_question_num=4, question_mode="likert"):
        self.testing = True
        self.task_name = "affect_reading"
        self.subject_id = subject_id
        self.task_presentor = task_presentor
        self.num_blocks = num_blocks
        self.affect_order = affect_order
        self.max_reading_time = max_reading_time
        self.readings = readings
        self.mult_choice_question_num = mult_choice_question_num
        self.question_mode = question_mode

        self.question_factory = QuestionFactory(self.task_presentor, mode=self.question_mode)

        self.max_reading_time = 10

        self.question_timeouts = {"slider alert": 6,
                                  "slider affect": 6,
                                  "slider mind_wandering": 6,
                                  "slider mult_choice": 30}

        self.question_timer = core.CountdownTimer(self.question_timeouts["slider alert"])

        assert (self.num_blocks == len(self.readings)) and (self.num_blocks == len(self.affect_order))

        self.instructions = self.task_presentor.read_instructions_from_file(self.task_name)
        self.mouse = event.Mouse()
        self.question_dict = self.read_question_dfs(self.readings)


    def run_full_task(self):

        self.task_presentor.display_instructions(self.instructions)

        for block in range(self.num_blocks):
            if self.testing:
                self.run_test(affect_condition=self.affect_order[block],
                               block_num=block,
                               reading=self.readings[block])
            else:
                self.run_block(affect_condition=self.affect_order[block],
                               block_num=block,
                               reading=self.readings[block])


    def parse_question_df(self, df):

        rows_dict = {}
        for row in df.iterrows():
            rows_dict[row[0]] = row[1].to_dict()

        return rows_dict


    def read_question_dfs(self, readings=[]):

        question_dict = {}
        for r in readings:
            df = pd.read_csv(f"./resources/affect_reading_questions/{r}_rote_questions.csv")
            question_dict[r] = self.parse_question_df(df)

        return question_dict


    def score_mult_choice(self, selection, question_answers, mult_choice_data):

        if question_answers[int(selection) - 1] == mult_choice_data["CorrectAnswer"]:
            return 1
        else:
            return 0


    def display_sliding_scale(self, type="alert", block_num=0,
                              mult_choice_data={}):

        if type == "mult_choice":
            self.question_factory.create_question(type, mult_choice_data=mult_choice_data)
        else:
            self.question_factory.create_question(type)

        slider_reset_time = self.question_timeouts[f"slider {type}"]
        self.question_timer.reset(slider_reset_time)

        self.question_factory.display_question(self.question_timer)
        self.task_presentor.logger.write_data_row(self.question_factory.get_data_line(self.subject_id, block_num))


    def display_affect_induction(self, affect_string):

        fpath = f"./resources/affect_videos/{affect_string}.mp4"
        movie_stim = visual.MovieStim3(win=self.task_presentor.window, filename=fpath)

        movie_clock = core.CountdownTimer(movie_stim.duration)

        while movie_clock.getTime() > 0:

            self.task_presentor.display_stim(movie_stim)


    def parse_text_from_file(self, text_name):

        fname = f"./resources/affect_reading_texts/{text_name}_reading.txt"

        with open (fname, 'r') as in_file:
            return in_file.readlines()


    def run_page(self, page_text, block_num, text_name, start_time, timer, page_num):

        size_mult = 0.8

        display_text = visual.TextStim(self.task_presentor.window,
                                       text=page_text,
                                       height=(0.1*size_mult),
                                       color=self.task_presentor.globals.default_text_color)
        self.task_presentor.display_drawer.add_to_draw_list(display_text)
        self.task_presentor.display_drawer.add_to_draw_list(self.task_presentor.advance_text)
        self.task_presentor.display_drawer.draw_all()
        self.task_presentor.window.flip()

        self.task_presentor.input_handler.handle_button_input("default", timer=timer)

        page_time = start_time - timer.getTime()

        self.task_presentor.logger.write_data_row([self.subject_id,
                                                   time.time(),
                                                   page_time,
                                                   block_num,
                                                   f"reading_{text_name}_page_{page_num + 1}",
                                                   page_text,
                                                   [],
                                                   [],
                                                   -1,
                                                   "None",
                                                   -1])




    def run_reading_task(self, text_name, block_num):

        text_lines = self.parse_text_from_file(text_name)
        total_reading_timer = core.CountdownTimer(self.max_reading_time)


        while total_reading_timer.getTime() > 0: # While they still have time to read the ENTIRE text.
            for indx, page in enumerate(text_lines):
                self.run_page(page, block_num, text_name, total_reading_timer.getTime(),total_reading_timer, indx)
                print(total_reading_timer.getTime())
                if total_reading_timer.getTime() < 0:
                    break
            # Finish Early.
            break



    def run_mult_choice_block(self, block_num, reading_name, randomize_presentation=True):

        question_data = {}
        order = [elm for elm in range(self.mult_choice_question_num)]

        if randomize_presentation:
            random.shuffle(order)

        for question in order:
            self.display_sliding_scale(type="mult_choice",
                                       block_num=block_num,
                                       mult_choice_data=self.question_dict[reading_name][question])


    def run_block(self, affect_condition="happy", block_num=0, reading=""):

        self.display_sliding_scale(type="alert", block_num=block_num)
        self.display_sliding_scale(type="affect",block_num=block_num)
        self.task_presentor.run_isi(random.choice([3, 5])) # Runs a fixation.

        # If No affect condition --- don't run video.
        if affect_condition != "none":
            self.display_affect_induction(affect_condition)

        self.task_presentor.run_isi(random.choice([4, 2])) # Runs a fixation.
        self.display_sliding_scale(type="affect")
        self.display_sliding_scale(type="alert")
        self.run_reading_task(reading)
        self.task_presentor.run_isi(random.choice([3, 5])) # Runs a fixation.
        self.display_sliding_scale(type="mind_wandering")
        self.run_mult_choice_block(block_num, reading, randomize_presentation=True)
        self.task_presentor.run_isi(random.choice([4, 2]))


    def run_test(self, affect_condition="happy", block_num=0, reading=""):

        self.display_sliding_scale(type="alert", block_num=block_num)
        self.display_sliding_scale(type="affect",block_num=block_num)
        self.display_sliding_scale(type="affect", block_num=block_num)
        self.display_sliding_scale(type="alert", block_num=block_num)
        self.run_reading_task(reading, block_num)
        self.display_sliding_scale(type="mind_wandering", block_num=block_num)
        self.run_mult_choice_block(block_num, reading, randomize_presentation=True)
        self.task_presentor.run_isi(random.choice([1, 2]))
