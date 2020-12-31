import random
import numpy as np

from psychopy import visual, core, event
from psychopy import prefs

# My imports.
from task_factory import TaskFactory
from globals import PsychopyGlobals
from data_logger import DataLogger

from lsl_trigger import LSLTriggerHandler
from parameters.trigger_dict import trigger_dict, trigger_string_dict

import sys

class TaskPresentor(object):
    def __init__(self, subject_id, task_list=["affect_reading", "finger_tapping", "stroop", "end"]):
        self.subject_id = subject_id
        self.task_list = task_list
        self.globals = PsychopyGlobals()
        self.task_factory = TaskFactory(self.subject_id, self)
        self.trigger_handler = LSLTriggerHandler()
        self.window = self.globals.window
        self.display_drawer = self.globals.the_drawer
        self.advance_text = self.globals.advance_text
        self.fixation_cross = self.globals.fixation_cross
        self.logger = DataLogger(self.subject_id, self.task_list[0])


        for task in task_list:
            if task == "end":
                self.run_end()
            task_obj = self.task_factory.create_task(task)
            self.logger.set_current_task(task)
            task_obj.run_full_task()
            del task_obj
            del self.logger


    def run_end(self):

        end_text = visual.TextStim(self.window, text="Thank you for completing all of the tasks")
        self.display_drawer.add_to_draw_list(end_text)
        self.display_drawer.add_to_draw_list(self.advance_text)
        self.display_drawer.draw_all()
        self.window.flip()

        while event.getKeys():
            continue

        sys.exit()


### Insturctions ---------------------------------------------------------------


    def read_instructions_from_file(self, task):

        fname = f"./instructions/{task}_instructions.txt"

        with open (fname, 'r') as in_file:
            return in_file.readlines()


    def display_instructions(self, instructions, return_bool=False):

        for text_prompt in instructions:
            display_text = visual.TextStim(self.window, text=text_prompt)
            self.display_drawer.add_to_draw_list(display_text)
            self.display_drawer.add_to_draw_list(self.advance_text)
            self.display_drawer.draw_all()
            self.window.flip()
            while not event.getKeys(keyList=['space']):
                continue

        if return_bool:
            return True


### Basic Stim Display ---------------------------------------------------------


    def run_ibi(self, ibi_time):

        self.display_drawer.add_to_draw_list(self.fixation_cross)
        self.display_drawer.draw_all()
        self.window.flip()
        core.wait(ibi_time)


    def run_isi(self, isi_time):

        self.display_drawer.add_to_draw_list(self.fixation_cross)
        self.display_drawer.draw_all()
        self.window.flip()
        core.wait(isi_time)


    def display_stim(self, stim):

        self.display_drawer.add_to_draw_list(stim)
        self.display_drawer.draw_all()
        self.window.flip()


    def display_focus(self, focus_time=2, instead_focus="+", resting=False):

        if resting:
            self.trigger_handler.send_int_trigger(trigger_string_dict["Rest_Start"])
        visual.TextStim(self.win, text=instead_focus).draw()
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
            return list(np.random.choice(dist, size=isi_amt))


### Big Brain Stuff ------------------------------------------------------------


    def shuffle_conditions(self, repeat_amt, conditions_list):

        shuffled_list = []
        for repeat in range(repeat_amt):
            random.shuffle(conditions_list)
            shuffled_list.append(conditions_list)

        flattened = [item for sublist in shuffled_list for item in sublist]

        return flattened


    def draw_and_wait_for_input(self, what_to_draw=[]):

        what_to_draw.append(self.advance_text)
        for stim in what_to_draw:
            self.display_drawer.add_to_draw_list(stim)
        self.display_drawer.draw_all()
        self.window.flip()

        while not event.getKeys():
            pass
        return


if __name__ == "__main__":
    print("Don't run this file :)")
