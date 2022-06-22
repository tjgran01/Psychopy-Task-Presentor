from task_presentor import TaskPresentor

from psychopy import gui
import sys

import pandas as pd
import time

import create_default_params_files

def main(task_list):
    myDlg = gui.Dlg(title="Participant ID Entry Field")

    myDlg.addText('Please enter the Participant ID for this session:')
    myDlg.addField('Participant ID:', "XXXX")

    myDlg.addText('What template will this participant be running through.')
    myDlg.addField('Bad Videos', choices=["Blue", "White"])
    myDlg.addField('Full Screen?', choices=["Yes", "No"])
    myDlg.addField('Practice', choices=["Yes", "No"])
    myDlg.addField('Task', choices=["emotional_anticipation", "episodic_prospection", "social_self_control", "non_social_self_control"])
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
    elif sub_id[-2] == "social_self_control":
        task_list = ["social_self_control", "end"]
    elif sub_id[-2] == "non_social_self_control":
        task_list = ["non_social_self_control", "end"]
    else:
        task_list = ["episodic_prospection", "end"]

    tp = TaskPresentor(sub_id[0], task_list=task_list, present_method="mri",
                task_template="Lighter Cue", full_screen=sub_id[-4],
                practice=sub_id[-3], lang=sub_id[-1],
                cue_cond=sub_id[-5])

if __name__ == "__main__":
    create_default_params_files.set_defaults()
    time.sleep(3)
    task_list = ["emotional_anticipation", "end"]
    main(task_list)
