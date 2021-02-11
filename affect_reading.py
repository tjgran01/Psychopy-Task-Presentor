import random
from psychopy import visual, core, event

import time
import pandas as pd

from psychopy_questions import QuestionFactory
from loggers.timing_logger import TimingLogger

class AffectReadingTask(object):
    def __init__(self, subject_id, task_presentor, num_blocks=4, affect_order=["happy", "none", "happy", "none"],
                 max_reading_time=180, readings=["hypotheses", "causalclaims", "validity", "variables"],
                 mult_choice_question_num=4, question_mode="likert", snap_questions=False,
                 randomize_question_presentation=True, movie_size_mult=2, text_size_mult=0.7,
                 affect_induction_time=150, default_fixation_time=2, question_timeouts={},
                 testing=False, use_padding=False, video_text_timer_prompt=3, reading_text_timer_prompt=3,
                 template_var="A"):
        self.task_name = "affect_reading"
        self.subject_id = subject_id
        self.task_presentor = task_presentor
        self.num_blocks = num_blocks
        self.affect_order = affect_order
        self.max_reading_time = max_reading_time
        self.readings = readings
        self.mult_choice_question_num = mult_choice_question_num

        self.question_mode = question_mode
        self.text_size_mult = text_size_mult
        self.randomize_mult_choice_presentation = randomize_question_presentation
        self.snap_questions = snap_questions
        self.randomize_question_presentation = randomize_question_presentation
        self.movie_size_mult = movie_size_mult

        #### These need to be added to param dict.
        self.affect_induction_time = affect_induction_time
        self.default_fixation_time = default_fixation_time
        self.testing = testing
        self.use_padding = use_padding
        self.template_var = self.task_presentor.task_template


        if self.task_presentor.present_method == "nirs":
            if self.template_var[0] == "A":
                self.template_var = "B"
            elif self.template_var[0] == "B":
                self.template_var ="A"

        self.readings = self.readings[self.template_var]

        self.question_factory = QuestionFactory(self.task_presentor,
                                                mode=self.question_mode,
                                                snap_for_all=self.snap_questions)

        self.question_timeouts = question_timeouts

        self.question_timer = core.CountdownTimer(self.question_timeouts["slider alert"])

        self.video_text_timer = core.CountdownTimer(video_text_timer_prompt)
        self.reading_text_timer = core.CountdownTimer(reading_text_timer_prompt)

        self.instructions = self.task_presentor.read_instructions_from_file(self.task_name)
        self.mouse = event.Mouse()
        self.question_dict = self.read_question_dfs(self.readings)

        self.timing_logger = TimingLogger(self.subject_id)

        self.movies = self.load_movies()
        self.movie_indx = 0




    def load_movies(self):

        movies = []
        for elm in self.affect_order:
            if elm != "none":
                print(f"Loading Movie File: ./resources/affect_videos/{elm}{self.template_var}.mp4")
                fpath = f"./resources/affect_videos/{elm}{self.template_var}.mp4"
                movie_stim = visual.MovieStim3(win=self.task_presentor.window,
                                               filename=fpath)

                #set size.
                movie_stim.size = [movie_stim.size[0] * self.movie_size_mult, movie_stim.size[1] * self.movie_size_mult]
                movies.append(movie_stim)

        return movies



    def run_full_task(self):

        self.task_presentor.display_experimenter_wait_screen("experimenter")

        self.display_sliding_scale(type="practice_slider", practice=True)
        self.display_sliding_scale(type="practice_mult_choice", practice=True)
        self.task_presentor.display_instructions(self.instructions, input_method="mouse")
        self.task_presentor.draw_wait_for_scanner()

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
                              mult_choice_data={}, practice=False):

        if type == "mult_choice":
            self.question_factory.create_question(type, mult_choice_data=mult_choice_data)
            self.task_presentor.trigger_handler.send_string_trigger("Mult_Choice_Question_Presented")
        else:
            self.task_presentor.trigger_handler.send_string_trigger("Slider_Question_Presented")
            self.question_factory.create_question(type)

        slider_reset_time = self.question_timeouts[f"slider {type}"]
        self.question_timer.reset(slider_reset_time)

        self.question_factory.display_question(self.question_timer)

        if not practice:
            self.task_presentor.logger.write_data_row(self.question_factory.get_data_line(self.subject_id, block_num))

        self.task_presentor.trigger_handler.send_string_trigger("Slider_Question_Answered")

        return self.question_timer.getTime()


    def display_timed_prompt(self, type=""):

        if type == "video":
            fname = f"./instructions/video_instructions.txt"
            m_timer = self.video_text_timer
        else:
            fname = f"./instructions/reading_instructions.txt"
            m_timer = self.reading_text_timer

        m_timer.reset()

        with open (fname, 'r') as in_file:
            lines = in_file.read()

        display_stim = visual.TextStim(self.task_presentor.window,
                                            text=lines,
                                            colorSpace='rgb')

        self.task_presentor.display_drawer.add_to_draw_list(display_stim)
        self.task_presentor.display_drawer.draw_all()
        self.task_presentor.window.flip()

        while m_timer.getTime() > 0:
            continue


    def display_affect_induction(self, affect_string):

        self.display_timed_prompt(type="video")

        movie_stim = self.movies[self.movie_indx]

        movie_clock = core.CountdownTimer(movie_stim.duration)
        affect_clock = core.CountdownTimer(self.affect_induction_time)

        print(f"MOVIE DURATION: {movie_stim.duration}")

        self.task_presentor.trigger_handler.send_string_trigger("Affect_Induction_Start")
        while movie_clock.getTime() > 0 and affect_clock.getTime() > 0:

            self.task_presentor.display_stim(movie_stim)

        self.task_presentor.trigger_handler.send_string_trigger("Affect_Induction_End")


    def parse_text_from_file(self, text_name):

        fname = f"./resources/affect_reading_texts/{text_name}_reading.txt"

        with open (fname, 'r') as in_file:
            lines = in_file.readlines()
            split_lines = [line.split(". ") for line in lines]

            all_lines = []
            for text in split_lines:
                for line in text:
                    all_lines.append(line)

            lines = []
            for line in all_lines:
                if not line.endswith("\n"):
                    if not line.endswith("."):
                        lines.append(f"{line}.")
                    else:
                        lines.append(line)
                else:
                    lines.append(line)


            return lines


    def run_page(self, page_text, block_num, text_name, start_time, timer, page_num):

        display_text = visual.TextStim(self.task_presentor.window,
                                       text=page_text,
                                       height=(0.1*self.text_size_mult),
                                       color=self.task_presentor.globals.default_text_color,
                                       alignText="left",
                                       pos=(0.0, 0.0))
        self.task_presentor.display_drawer.add_to_draw_list(display_text)
        # self.task_presentor.display_drawer.add_to_draw_list(self.task_presentor.advance_text)
        self.task_presentor.display_drawer.draw_all()
        self.task_presentor.window.flip()

        # Needs to be changed to MOUSE.
        self.task_presentor.input_handler.handle_mouse_input("left", timer=timer)

        self.task_presentor.trigger_handler.send_string_trigger("Page_Turn")

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

        self.display_timed_prompt(type="reading")

        self.task_presentor.trigger_handler.send_string_trigger("Reading_Section_Began")

        while total_reading_timer.getTime() > 0: # While they still have time to read the ENTIRE text.
            for indx, page in enumerate(text_lines):
                self.run_page(page, block_num, text_name, total_reading_timer.getTime(),total_reading_timer, indx)
                if total_reading_timer.getTime() < 0:
                    break
            # Finish Early.
            break

        self.task_presentor.trigger_handler.send_string_trigger("Reading_Section_Ended")

        return total_reading_timer.getTime()



    def run_mult_choice_block(self, block_num, reading_name, randomize_presentation=True):

        time_left = 0
        question_data = {}
        order = [elm for elm in range(self.mult_choice_question_num)]

        if randomize_presentation:
            random.shuffle(order)

        for question in order:
            scale_time = self.display_sliding_scale(type="mult_choice",
                                                    block_num=block_num,
                                                    mult_choice_data=self.question_dict[reading_name][question])

            self.timing_logger.write_row([self.subject_id, "mult-choice", scale_time, block_num])

        return time_left


    def determine_fixation_time(self, time_left=0):

        if self.use_padding == False:
            return self.default_fixation_time
        else:
            return self.default_fixation_time + time_left


    def run_block(self, affect_condition="happy", block_num=0, reading=""):

        # This will be passed to fixation for padding.
        time_left = self.display_sliding_scale(type="affect", block_num=block_num)
        self.timing_logger.write_row([self.subject_id, "affect", time_left, block_num])

        self.task_presentor.run_isi(self.determine_fixation_time(time_left=time_left)) # Runs a fixation.

        # If No affect condition --- don't run video --- don't run post fixation video.
        if affect_condition != "none":
            self.display_affect_induction(affect_condition)
            self.task_presentor.run_isi(self.determine_fixation_time()) # Runs a fixation after affect induction.
            time_left = self.display_sliding_scale(type="affect") # Runs an addition affect prompt.
            self.timing_logger.write_row([self.subject_id, "affect", time_left, block_num])
            self.task_presentor.run_isi(self.determine_fixation_time(time_left=time_left))

        time_left = 0

        time_left += self.run_reading_task(reading, block_num)
        self.timing_logger.write_row([self.subject_id, f"reading-{reading}", time_left, block_num])
        self.task_presentor.run_isi(self.determine_fixation_time()) # Runs a fixation.
        scale_time = self.display_sliding_scale(type="mind_wandering")
        time_left += scale_time
        self.timing_logger.write_row([self.subject_id, f"mind_wandering", scale_time, block_num])
        time_left += self.run_mult_choice_block(block_num, reading,
                                                randomize_presentation=self.randomize_question_presentation)

        self.task_presentor.run_isi(self.determine_fixation_time(time_left=time_left))


    def run_slider_tut(self):

        self.display_sliding_scale(type="alert", block_num=0)
        self.display_sliding_scale(type="affect",block_num=0)
        self.run_mult_choice_block(0, "causalclaims",randomize_presentation=self.randomize_question_presentation)


    def run_test(self, affect_condition="happy", block_num=0, reading=""):

        if affect_condition != "none":
            self.display_affect_induction(affect_condition)


        # self.display_sliding_scale(type="alert", block_num=block_num)
        # self.display_sliding_scale(type="affect",block_num=block_num)
        # self.display_sliding_scale(type="affect", block_num=block_num)
        # self.display_sliding_scale(type="alert", block_num=block_num)
        # self.run_reading_task(reading, block_num)
        # self.display_sliding_scale(type="mind_wandering", block_num=block_num)
        # self.run_mult_choice_block(block_num, reading, randomize_presentation=True)
        # self.task_presentor.run_isi(random.choice([1, 2]))
