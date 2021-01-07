import random
from psychopy import visual, core, event

import time
import pandas as pd

class AffectReadingTask(object):
    def __init__(self, subject_id, task_presentor, num_blocks=4, affect_order=["happy", "none", "happy", "none"],
                 max_reading_time=180, readings=["hypotheses", "causalclaims", "validity", "variables"],
                 mult_choice_question_num=4):
        self.testing = True
        self.task_name = "affect_reading"
        self.subject_id = subject_id
        self.task_presentor = task_presentor
        self.num_blocks = num_blocks
        self.affect_order = affect_order
        self.max_reading_time = max_reading_time
        self.readings = readings
        self.mult_choice_question_num = mult_choice_question_num

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

        self.export_data()


    def parse_question_df(self, df):

        rows_dict = {}
        for row in df.iterrows():
            rows_dict[row[0]] = row[1].to_dict()

        return rows_dict


    def read_question_dfs(self, readings=[]):

        question_dict = {}
        for r in readings:
            df = pd.read_csv(f"./resources/affect_reading_questions/{r}_rote_questions.csv", sep="\t")
            question_dict[r] = self.parse_question_df(df)

        return question_dict


    def score_mult_choice(self, selection, question_answers, mult_choice_data):

        if question_answers[int(selection) - 1] == mult_choice_data["CorrectAnswer"]:
            return 1
        else:
            return 0


    def display_sliding_scale(self, type="alert", block_num=0,
                              mult_choice_data={}):

        m_question_text = ""

        if type == "alert":

            m_text = "Please indicate your current level of alertness at this time."
            m_ticks = [1,2,3,4,5,6,7]
            m_labels = ["Extremely Sleepy", "", "", "Neutral", "", "", "Extremely Alert"]
            m_style = "triangleMarker"
            m_size = [1.0, 0.1]
            m_pos = (0.0, 0.0)
            m_flip = False

        elif type == "affect":

            m_text = "Please Indicate the extent to which you feel happy or sad currently."
            m_ticks = [1,2,3,4,5,6,7]
            m_labels = ["Extremely Sad", "", "", "Neutral", "", "", "Extremely Happy"]
            m_style = "rating"
            m_size = [1.0, 0.1]
            m_pos = (0.0, 0.0)
            m_flip = False

        elif type == "mult_choice":

            m_text = mult_choice_data["InstructionText"]
            m_question_text = mult_choice_data["QuestionText"]
            m_ticks = [1,2,3,4]
            question_answers = [mult_choice_data["CorrectAnswer"],
                                mult_choice_data["AnswerOption2"],
                                mult_choice_data["AnswerOption3"],
                                mult_choice_data["AnswerOption4"]]
            random.shuffle(question_answers)
            m_labels = question_answers
            m_style = "myRadio"
            m_size = [0.06, 0.6]
            m_pos = (-0.9, -0.5)
            m_flip = True

        elif type == "mind_wandering":

            m_text = "Please indicate how much you were zoning out while reading the text."
            m_ticks = [1, 2]
            m_labels = ["Yes", "No"]
            m_style = "rating"
            m_size = [1.0, 0.1]
            m_pos = (0.0, 0.0)
            m_flip = False

        text_stim = visual.TextStim(win=self.task_presentor.window,
                                    text=m_text, pos=(0, .8))
        slider = visual.Slider(win=self.task_presentor.window,
                               ticks=m_ticks,
                               labels=m_labels,
                               style=m_style,
                               size=m_size,
                               pos=m_pos,
                               flip=m_flip)

        slider.markerPos = random.choice(m_ticks)

        if m_question_text:
            question_text_stim = visual.TextStim(win=self.task_presentor.window,
                                                 text=m_question_text, pos=(-0.2, .3))
            stim_list = [question_text_stim, text_stim, slider]
        else:
            stim_list = [text_stim, slider]

        self.task_presentor.display_stims(stim_list)

        while not slider.getRating():
            core.wait(.1)
            y_change =  self.mouse.getWheelRel()[1]
            if y_change != 0.0:
                slider.markerPos += y_change
                self.task_presentor.display_stims(stim_list)
            if self.mouse.getPressed()[0] == 1:
                slider.recordRating(slider.markerPos)
                selection = slider.getRating()
                if type == "mult_choice":
                    score = self.score_mult_choice(selection,
                                                   question_answers,
                                                   mult_choice_data)
                else:
                    score = -1
                self.task_presentor.logger.write_data_row([self.subject_id,
                                                           time.time(),
                                                           slider.getRT(),
                                                           block_num,
                                                           type,
                                                           m_question_text,
                                                           m_ticks,
                                                           m_labels,
                                                           selection,
                                                           m_labels[int(selection)-1],
                                                           score])



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


    def run_page(self, page_text, block_num, text_name, start_time, timer):

        size_mult = 0.8

        display_text = visual.TextStim(self.task_presentor.window,
                                       text=page_text,
                                       height=(0.1*size_mult))
        self.task_presentor.display_drawer.add_to_draw_list(display_text)
        self.task_presentor.display_drawer.add_to_draw_list(self.task_presentor.advance_text)
        self.task_presentor.display_drawer.draw_all()
        self.task_presentor.window.flip()
        while not event.getKeys(keyList=['space']):
            continue

        page_time = start_time - timer.getTime()

        self.task_presentor.logger.write_data_row([self.subject_id,
                                                   time.time(),
                                                   page_time,
                                                   block_num,
                                                   f"reading_{text_name}",
                                                   page_text,
                                                   [],
                                                   [],
                                                   [],
                                                   [],
                                                   -1])




    def run_reading_task(self, text_name, block_num):

        text_lines = self.parse_text_from_file(text_name)
        total_reading_timer = core.CountdownTimer(self.max_reading_time)


        while total_reading_timer.getTime() > 0: # While they still have time to read the ENTIRE text.
            for page in text_lines:
                self.run_page(page, block_num, text_name, total_reading_timer.getTime(),total_reading_timer)
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
