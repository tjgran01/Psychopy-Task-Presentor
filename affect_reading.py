import random
from psychopy import visual, core, event

import time

class AffectReadingTask(object):
    def __init__(self, subject_id, task_presentor, num_blocks=2, affect_order=["happy", "sad"], max_reading_time=180):
        self.task_name = "affect_reading"
        self.subject_id = subject_id
        self.task_presentor = task_presentor
        self.num_blocks = num_blocks
        self.affect_order = affect_order
        self.max_reading_time = max_reading_time
        self.instructions = self.task_presentor.read_instructions_from_file(self.task_name)
        self.mouse = event.Mouse()
        self


    def run_full_task(self):

        self.task_presentor.display_instructions(self.instructions)

        for block in range(self.num_blocks):
            self.run_block(affect_condition=self.affect_order[block], block_num=block)

        self.export_data()


    def display_sliding_scale(self, type="alert", block_num=0):

        if type == "alert":

            m_text = "Please indicate your current level of alertness at this time."
            m_ticks = [1,2,3,4,5,6,7]
            m_labels = ["Extremely Sleepy", "", "", "Neutral", "", "", "Extremely Alert"]
            m_style = "triangleMarker"
            m_size = [1.0, 0.1]

        elif type == "affect":

            m_text = "Please Indicate the extent to which you feel happy or sad currently."
            m_ticks = [1,2,3,4,5,6,7]
            m_labels = ["Extremely Sad", "", "", "Neutral", "", "", "Extremely Happy"]
            m_style = "rating"
            m_size = [1.0, 0.1]

        elif type == "mult_choice":

            m_text = "Please indicate your response for the following question using the choices provided below."
            m_ticks = [1,2,3,4]
            m_labels = ["a - {whatever the question text }", "b", "c", "d"]
            m_style = "radio"
            m_size = [0.1, 1.0]

        elif type == "mind_wandering":

            m_text = "Please indicate how much you were zoning out while reading the text."
            m_tick = [1, 2]
            m_labels = ["Yes", "No"]
            m_style = "rating"
            m_size = [1.0, 0.1]

        text_stim = visual.TextStim(win=self.task_presentor.window,
                                    text=m_text, pos=(0, .8))
        slider = visual.Slider(win=self.task_presentor.window,
                               ticks=m_ticks,
                               labels=m_labels,
                               style=m_style,
                               size=m_size)

        print(slider.size)
        slider.markerPos = 4

        self.task_presentor.display_stims([slider, text_stim])

        while not slider.getRating():
            core.wait(.1)
            y_change =  self.mouse.getWheelRel()[1]
            if y_change != 0.0:
                slider.markerPos += y_change
                self.task_presentor.display_stims([slider, text_stim])
            if self.mouse.getPressed()[0] == 1:
                slider.recordRating(slider.markerPos)
                self.task_presentor.logger.write_data_row([self.subject_id,
                                                           time.time(),
                                                           slider.getRT(),
                                                           block_num,
                                                           type,
                                                           m_ticks,
                                                           "||".join(m_labels),
                                                           slider.getRating(),
                                                           None])



    def display_affect_induction(self, affect_string):

        fpath = f"./resources/affect_videos/{affect_string}.mp4"
        movie_stim = visual.MovieStim3(win=self.task_presentor.window, filename=fpath, size=[])

        movie_clock = core.CountdownTimer(movie_stim.duration)

        while movie_clock.getTime() > 0:

            self.task_presentor.display_stim(movie_stim)


    def parse_text_from_file(self, text_name):

        fname = f"./resources/affect_reading_texts/{text_name}_reading.txt"

        with open (fname, 'r') as in_file:
            return in_file.readlines()


    def run_reading_task(self, text_name):

        text_lines = self.parse_text_from_file(text_name)
        total_reading_timer = core.CountdownTimer(self.max_reading_time)

        while total_reading_timer.getTime() > 0: # While they still have time to read the ENTIRE text.
            if self.task_presentor.display_instructions(text_lines, return_complete=True): # If they finish early.
                break


    def run_block(self, affect_condition="happy", block_num=0):

        # self.display_sliding_scale(type="alert", block_num=block_num)
        # self.display_sliding_scale(type="affect",block_num=block_num)
        # self.task_presentor.run_isi(random.choice([3, 5])) # Runs a fixation.
        # self.display_affect_induction(affect_condition)
        # self.task_presentor.run_isi(random.choice([4, 2])) # Runs a fixation.
        # self.display_sliding_scale(type="alert")
        # self.display_sliding_scale(type="affect")
        # self.task_presentor.run_isi(random.choice([3, 5])) # Runs a fixation.
        self.run_reading_task("scientific_method")
        # self.display_sliding_scale(type="mind_wandering")
        # self.display_sliding_scale(type="multiple_choice")
        # self.task_presentor.run_isi(random.choice([4, 2]))
