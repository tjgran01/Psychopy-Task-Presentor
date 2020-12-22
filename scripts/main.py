from stroop import StroopTask
from psychopy import gui
import sys

import pandas as pd


def main():
    myDlg = gui.Dlg(title="Participant ID Entry Field")
    myDlg.addText('Please enter the Participant ID for this session:')
    myDlg.addField('Participant ID:', "XXXX")
    sub_id = myDlg.show()  # show dialog and wait for OK or Cancel
    if not myDlg.OK:  # or if ok_data is not None
        sys.exit()

    # Try to load preferences from file.
    try:
        prefs = pd.read_csv("../preferences/id_preference_table.csv", dtype={"sub_id": str})
        prefs.set_index("sub_id", inplace=True)
        prefs = prefs.loc[sub_id].to_dict(orient='records')
        st = StroopTask(sub_id[0], num_blocks=prefs[0]["num_blocks"],
                        fixation_time=prefs[0]["fixation_time"],
                        congruence_rate=prefs[0]["congruence_rate"],
                        num_trials=prefs[0]["num_trials"],
                        ibi_time=prefs[0]["ibi_time"],
                        variable_isi=prefs[0]["variable_isi"])
    except:
        print("No preference file found (or preferences file is missing specified Subject ID.)")
        print("Running with Default Arguments")
        st = StroopTask(sub_id[0])

if __name__ == "__main__":
    main()
