import random
import numpy as np

from psychopy import visual, core, event
from psychopy import prefs

# My imports.
from task_factory import TaskFactory
from globals import PsychopyGlobals
from loggers.data_logger import DataLogger
from loggers.trigger_logger import TriggerLogger
from input_handler import InputHandler

from lsl_trigger import LSLTriggerHandler
from parameters.trigger_dict import trigger_dict, trigger_string_dict

import sys

class TaskPresentor(object):
    def __init__(self, subject_id, task_list=["finger_tapping", "end"],
                 present_method="mri", run_task_list=True, task_template=None,
                 full_screen=True, practice=False):
        self.subject_id = subject_id
        self.task_list = task_list
        self.full_screen = full_screen
        self.practice = practice
        print(f"TASK PRESENTER PRACTICE MODE: {self.practice}")
        self.globals = PsychopyGlobals(full_screen=self.full_screen)
        self.task_factory = TaskFactory(self.subject_id, self)
        self.input_handler = InputHandler(mode=present_method)
        self.window = self.globals.window
        self.window.mouseVisible = False
        self.display_drawer = self.globals.the_drawer
        self.advance_text = self.globals.advance_text
        self.fixation_cross = self.globals.fixation_cross
        self.logger = DataLogger(self.subject_id, self.task_list[0])
        self.trigger_logger = TriggerLogger(self.subject_id)
        self.trigger_handler = LSLTriggerHandler(logger=self.trigger_logger)

        self.present_method = present_method
        self.task_template = task_template

        self.current_task = ""

        if run_task_list:

            for task in task_list:
                self.current_task = task
                if task == "end":
                    self.run_end()
                if task == "resting_state":
                    self.run_resting_state()
                    continue
                task_obj = self.task_factory.create_task(task, practice=self.practice)
                self.logger.set_current_task(task)
                task_obj.run_full_task()
                del task_obj

        else:
            self.task_obj = self.task_factory.create_task(task_list[0], practice=self.practice)
            self.logger.set_current_task(task_list[0])


    def run_end(self):

        event.clearEvents()

        end_text = visual.TextStim(self.window,
                                   text="Thank you for completing all of the tasks",
                                   color=self.globals.default_text_color)
        self.display_drawer.add_to_draw_list(end_text)
        self.display_drawer.add_to_draw_list(self.advance_text)
        self.display_drawer.draw_all()
        self.window.flip()

        while not event.getKeys():
            if self.input_handler.handle_mouse_input("left"):
                break
            continue

        sys.exit()


    def run_resting_state(self):

        event.clearEvents()

        self.display_experimenter_wait_screen("experimenter", force=True)

        self.run_isi((60 * 5), trigger=True)



### Insturctions ---------------------------------------------------------------

    def set_advance_text(self):

        if self.present_method == 'mri':
            if self.current_task != "affect_reading":
                m_text = "Press Index Finger Button to Continue."
            else:
                m_text = "Press Thumb Button to Continue."
        else:
            if self.current_task != "affect_reading":
                m_text = "Press Spacebar Key to Continue."
            else:
                m_text = "Click Left Mouse Button to Continue."

        self.advance_text = visual.TextStim(self.window,
                                            text=m_text,
                                            colorSpace='rgb',
                                            color=(1.0, 0.0, 0.0),
                                            pos=(0.0, -0.6))



    def read_instructions_from_file(self, task):

        fname = f"./instructions/{task}_instructions_{self.present_method}.txt"

        with open (fname, 'r') as in_file:
            return in_file.readlines()


    def display_instructions(self, instructions, return_complete=False,
                             reading_task=False, input_method="key"):

        m_advance_text = self.set_advance_text()

        size_mult = 1.0

        self.trigger_handler.send_string_trigger("Instructions_Displayed")

        for text_prompt in instructions:
            display_text = visual.TextStim(self.window,
                                           text=text_prompt,
                                           height=(0.1*size_mult),
                                           color=self.globals.default_text_color)
            self.display_drawer.add_to_draw_list(display_text)
            self.display_drawer.add_to_draw_list(self.advance_text)
            self.display_drawer.draw_all()
            self.window.flip()
            if input_method == "mouse":
                self.input_handler.handle_mouse_input("left")
                self.trigger_handler.send_string_trigger("Page_Turn_Instructions")
            else:
                self.input_handler.handle_button_input("default")
                self.trigger_handler.send_string_trigger("Page_Turn_Instructions")


        if return_complete:
            return True


    def display_experimenter_wait_screen(self, key, force=False):

        if self.present_method == "mri" or force:

            size_mult = 1.0

            self.trigger_handler.send_string_trigger("Experimenter_Screen_Displayed")

            text_prompt = "The next task will begin shortly, please wait for the experimenter to advance to the next task."

            display_text = visual.TextStim(self.window,
                                           text=text_prompt,
                                           height=(0.1*size_mult),
                                           color=self.globals.default_text_color)
            self.display_drawer.add_to_draw_list(display_text)
            self.display_drawer.draw_all()
            self.window.flip()

            self.input_handler.handle_button_input(key)

            self.trigger_handler.send_string_trigger("Experimenter_Screen_Ended")



### Basic Stim Display ---------------------------------------------------------


    def run_ibi(self, ibi_time):

        self.display_drawer.add_to_draw_list(self.fixation_cross)
        self.display_drawer.draw_all()
        self.window.flip()
        core.wait(ibi_time)


    def run_isi(self, isi_time, trigger=False):

        if trigger:
            self.trigger_handler.send_string_trigger("Resting_State_Start")

        self.display_drawer.add_to_draw_list(self.fixation_cross)
        self.display_drawer.draw_all()
        self.window.flip()
        core.wait(isi_time)

        if trigger:
            self.trigger_handler.send_string_trigger("Resting_State_End")


    def display_stim(self, stim):

        self.display_drawer.add_to_draw_list(stim)
        self.display_drawer.draw_all()
        self.window.flip()


    def display_stims(self, stim_list):

        for stim in stim_list:
            self.display_drawer.add_to_draw_list(stim)
        self.display_drawer.draw_all()
        self.window.flip()


    def display_focus(self, focus_time=2, instead_focus="+", resting=False):

        if resting:
            self.trigger_handler.send_int_trigger(trigger_string_dict["Rest_Start"])
        visual.TextStim(self.win,
                        text=instead_focus,
                        color=self.globals.default_text_color).draw()
        self.win.flip()
        if self.focus_time > 0:
            core.wait(self.focus_time)
        else:
            core.wait(focus_time)

        if resting:
            self.trigger_handler.send_int_trigger(trigger_string_dict["Rest_End"])

### Creating Random ISI --------------------------------------------------------


    def create_variable_isi_list(self, isi_amt, fixation_time, how="gamma"):

        if how == "gamma":
            shape = fixation_time
            scale = fixation_time / 2
            dist = np.random.gamma(shape, scale, 1000)
        else:
            shape = fixation_time
            scale = fixation_time / 2
            dist = np.random.normal(shape, scale, 1000)
        return list(np.random.choice(dist, size=isi_amt))



    def sample_variable_isi(self, mean, std):

        dist = np.random.normal(mean, std, 1000)
        choice = np.random.choice(dist)
        print(choice)
        return np.random.choice(dist)





### Big Brain Stuff ------------------------------------------------------------


    def shuffle_conditions(self, repeat_amt, conditions_list):

        shuffled_list = []
        for repeat in range(repeat_amt):
            random.shuffle(conditions_list)
            shuffled_list.append(conditions_list)
        flattened = [item for sublist in shuffled_list for item in sublist]

        return flattened


    def draw_and_wait_for_input(self, what_to_draw=[]):

        event.clearEvents()

        what_to_draw.append(self.advance_text)
        for stim in what_to_draw:
            self.display_drawer.add_to_draw_list(stim)
        self.display_drawer.draw_all()
        self.window.flip()

        while not event.getKeys():
            pass
        return


    def draw_wait_for_scanner(self):

        event.clearEvents()

        if self.present_method == "mri":

            scanner_wait_text =  visual.TextStim(self.window,
                                                 text="Waiting for scanner event...",
                                                 color=self.globals.default_text_color)
            self.display_drawer.add_to_draw_list(scanner_wait_text)
            self.display_drawer.draw_all()
            self.window.flip()

            while not event.getKeys(keyList=["5", self.globals.ttl_key]):
                continue

            self.trigger_handler.send_string_trigger("Scanner_Start_Received")



if __name__ == "__main__":
    print("Don't run this file :)")
