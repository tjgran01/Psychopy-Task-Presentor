from re import sub
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
    myDlg.addText('What template will this participant be running through.')
    myDlg.addField('Bad Videos', choices=["light_to_dark", "dark_to_light"])
    myDlg.addField('Full Screen?', choices=["Yes", "No"])
    myDlg.addField('Practice', choices=["Yes", "No"])
    myDlg.addField('First Task', choices=["emotional_anticipation", "episodic_prospection"])
    myDlg.addField('Language', choices=["Deutsch", "English"])


    sub_id = myDlg.show()  # show dialog and wait for OK or Cancel
    if not myDlg.OK:  # or if ok_data is not None
        sys.exit()

    for elm in sub_id:
        if elm == "Yes":
            elm = True
        if elm == "No":
            elm = False

    if sub_id[-2] == "emotional_anticipation":
        task_list = ["emotional_anticipation", "end"]
    else:
        task_list = ["episodic_prospection", "end"]
    

    # if sub_id[1] == "nirs":
    #     task_list.insert(0, "resting_state")

    tp = TaskPresentor(sub_id[0], task_list=task_list, present_method="mri", 
                       task_template="Lighter Cue", full_screen=sub_id[-4], practice=sub_id[-3], lang=sub_id[-1], cue_cond=sub_id[-5])

if __name__ == "__main__":
    task_list = ["emotional_anticipation", "end"]
    #task_list = ["affect_reading", "end"]
    main(task_list)
