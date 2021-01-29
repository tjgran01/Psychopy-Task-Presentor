from task_presentor import TaskPresentor

from stroop import StroopTask
from psychopy import gui
import sys

import pandas as pd

import time


def main(task_list):
    myDlg = gui.Dlg(title="Participant ID Entry Field")
    myDlg.addText('Please enter the Participant ID for this session:')
    myDlg.addField('Participant ID:', "XXXX")
    sub_id = myDlg.show()  # show dialog and wait for OK or Cancel
    if not myDlg.OK:  # or if ok_data is not None
        sys.exit()

    tp = TaskPresentor(sub_id[0], task_list=task_list)

if __name__ == "__main__":

    task_list = ["finger_tapping", "stroop", "affect_reading", "end"]

    main(task_list)
