from psychopy import visual, event, core, gui
import sys
import os
import platform

from display_drawer import DisplayDrawer


### Might want to singleton this.
class PsychopyGlobals(object):
    """
    Stores all global attributes for running the BART application.
    Also contains methods and checks to ensure that those attributes
    are valid.

    Args:
        None
    Returns:
        None
    """

    def __init__(self, full_screen=False, presentation_mode="mri"):
        # PsychoPy Stuff.
        if platform.system() == "Windows":
            self.window = visual.Window(size=[1920 / 2 , 1080 / 2], monitor='testMonitor',
                                            color="black", fullscr=False,
                                            screen=1, allowGUI=True)
        else:
            self.window = visual.Window(size=[500, 500], monitor='testMonitor',
                                color="black", fullscr=False,
                                screen=1, allowGUI=True)

        self.ttl_key = "t"

        self.the_drawer = DisplayDrawer()
        self.default_text_color = [0,0,0]

        if presentation_mode == "mri":
            self.advance_btn_str = "Index Finger Button"
        else:
            self.advance_btn_str = "SPACEBAR"

        self.aspect_ratio = float(self.window.size[1]) / float(self.window.size[0])
        self.advance_text = visual.TextStim(self.window,
                                            text=f"Press '{self.advance_btn_str}' to advance to the next page.",
                                            colorSpace='rgb',
                                            color=(1.0, 0.0, 0.0),
                                            pos=(0.0, -0.6))
        self.fixation_cross = visual.TextStim(self.window,
                                              text="+",
                                              color=self.default_text_color)
