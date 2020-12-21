from stroop import StroopTask
from psychopy import gui
import sys


def main():
    myDlg = gui.Dlg(title="Participant ID Entry Field")
    myDlg.addText('Please enter the Participant ID for this session:')
    myDlg.addField('Participant ID:', "XXXX")
    sub_id = myDlg.show()  # show dialog and wait for OK or Cancel
    if not myDlg.OK:  # or if ok_data is not None
        sys.exit()

    st = StroopTask(subject_id=sub_id[0])

if __name__ == "__main__":
    main()
