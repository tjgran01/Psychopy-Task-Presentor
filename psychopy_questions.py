from psychopy import visual, core, event
import random

import pylink

import time

class QuestionFactory(object):
    def __init__(self, task_presentor, mode="likert"):
        self.task_presentor = task_presentor
        self.mode = mode
        self.mouse = event.Mouse()


    def get_data_line(self, subject_id, block_num):

        if self.type == "mult_choice":
            score = self.score_mult_choice()
        else:
            score = -1

        if self.timeout:
            rt = None
            selection = "TIMEOUT"
            score = -2
        else:
            rt = self.slider.getRT()
            selection = self.selction


        return [subject_id,
                time.time(),
                rt,
                block_num,
                self.type_text,
                self._question_text,
                self.m_ticks,
                self.m_labels,
                selection,
                self.m_labels[int(self.selection)-1],
                score]


    def score_mult_choice(self):

        if self.question_answers[int(self.selection) - 1] == self.mult_choice_data["CorrectAnswer"]:
            return 1
        else:
            return 0


    def create_question(self, type, mult_choice_data={}):

        self.m_question_text = ""
        self.mult_choice_data = mult_choice_data

        self.type = type

        if type == "alert":

            self.m_text = "Please indicate your current level of alertness at this time."
            self.m_ticks = [1,2,3,4,5,6,7]
            self.m_labels = ["Extremely Sleepy", "", "", "Neutral", "", "", "Extremely Alert"]
            self.m_style = "triangleMarker"
            self.m_size = [1.0, 0.1]
            self.m_pos = (0.0, 0.0)
            self.m_flip = False

        elif type == "affect":

            self.m_text = "Please Indicate the extent to which you feel happy or sad currently."
            self.m_ticks = [1,2,3,4,5,6,7]
            self.m_labels = ["Extremely Sad", "", "", "Neutral", "", "", "Extremely Happy"]
            self.m_style = "triangleMarker"
            self.m_size = [1.0, 0.1]
            self.m_pos = (0.0, 0.0)
            self.m_flip = False

        elif type == "mult_choice":

            self.m_text = mult_choice_data["InstructionText"]
            self.m_question_text = mult_choice_data["QuestionText"]
            self.m_ticks = [1,2,3,4]
            self.question_answers = [mult_choice_data["CorrectAnswer"],
                                     mult_choice_data["AnswerOption2"],
                                     mult_choice_data["AnswerOption3"],
                                     mult_choice_data["AnswerOption4"]]
            random.shuffle(self.question_answers)
            self.m_labels = self.question_answers
            self.m_style = "myRadio"
            self.m_size = [0.06, 0.6]
            self.m_pos = (-0.9, -0.5)
            self.m_flip = True
            self._question_text = self.m_question_text

        elif type == "mind_wandering":

            self.m_text = "Please indicate the extent to which you were 'zoning out' while reading the text."
            self.m_ticks = [1, 2]
            self.m_labels = ["Yes", "No"]
            self.m_style = "triangleMarker"
            self.m_size = [1.0, 0.1]
            self.m_pos = (0.0, 0.0)
            self.m_flip = False
            self._question_text = self.m_question_text

        if self.mode == "likert":
            stims = self.create_likert_question(type, self.m_text, self.m_ticks, self.m_labels,
                                                self.m_style, self.m_size, self.m_pos, self.m_flip,
                                                m_question_text=self.m_question_text)

        return stims



    def create_vas_question(self, labels):

        pass


    def create_likert_question(self, type, text, ticks, labels, style,
                               size, pos, flip, m_question_text=None):

        if type == "mult_choice":
            self.type_text = f"mult_choice_{self.mult_choice_data['Text']}_page_{self.mult_choice_data['PageNum']}"
        else:
            self.type_text = type
            self._question_text = text

        self.text_stim = visual.TextStim(win=self.task_presentor.window,
                                         text=text, pos=(0, .8),
                                         color=self.task_presentor.globals.default_text_color)
        self.slider = visual.Slider(win=self.task_presentor.window,
                                    ticks=ticks,
                                    labels=labels,
                                    style=style,
                                    size=size,
                                    pos=pos,
                                    flip=flip)

        self.slider.markerPos = random.choice(ticks)

        if self.m_question_text:
            self.question_text_stim = visual.TextStim(win=self.task_presentor.window,
                                                      text=m_question_text, pos=(-0.2, .3),
                                                      color=self.task_presentor.globals.default_text_color)
            self.stims = [self.slider, self.question_text_stim, self.text_stim]
        else:
            self.stims = [self.slider, self.text_stim]


    def display_question(self, question_timer):

        self.task_presentor.display_stims(self.stims)

        while not self.slider.getRating() and question_timer.getTime() > 0:
            core.wait(.1)
            y_change =  self.mouse.getWheelRel()[1]
            self.task_presentor.display_stims(self.stims)
            if y_change != 0.0:
                self.slider.markerPos += y_change
                self.task_presentor.display_stims(self.stims)
            if self.mouse.getPressed()[0] == 1:
                self.timeout = False
                self.slider.recordRating(self.slider.markerPos)
                self.selection = self.slider.getRating()
                if type == "mult_choice":
                    self._question_text = m_question_text
                    self.type_text = f"mult_choice_{self.mult_choice_data['Text']}_page_{self.mult_choice_data['PageNum']}"
                else:
                    self.type_text = self.type
                    self.score = -1
                    self._question_text = self.m_text

        self.timeout = True
