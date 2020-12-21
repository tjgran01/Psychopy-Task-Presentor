from psychopy import visual, event, core, gui
import sys
import os
import platform

from display_drawer import DisplayDrawer


### Might want to singleton this.
class StroopGlobals(object):
    """
    Stores all global attributes for running the BART application.
    Also contains methods and checks to ensure that those attributes
    are valid.

    Args:
        None
    Returns:
        None
    """

    def __init__(self, full_screen=True):
        # PsychoPy Stuff.
        if platform.system() == "Windows":
            self.window = visual.Window(size=[1920 / 2 , 1080 / 2], monitor='testMonitor',
                                            color=(0, 0, 0), fullscr=full_screen,
                                            screen=2, allowGUI=True)
        else:
            self.window = visual.Window(size=[1000, 500], monitor='testMonitor',
                                color=(0, 0, 0), fullscr=full_screen,
                                screen=2, allowGUI=True)

        # self.window.mouseVisible = False

        self.the_drawer = DisplayDrawer()

        self.aspect_ratio = float(self.window.size[1]) / float(self.window.size[0])
        self.instructions = self.read_instructions_from_file(fname="./instructions/stroop_instructions.txt")


    def read_instructions_from_file(self, fname="./instructions/instructions.txt"):

        with open (fname, 'r') as in_file:
            return in_file.readlines()
