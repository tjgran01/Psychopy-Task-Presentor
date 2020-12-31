import pickle

#### EDIT THIS TO EDIT DEFAULT PARAMETERS.

stroop_defaults = {
                   "num_blocks": 2,
                   "fixation_time": 2,
                   "congruence_rate": .2,
                   "num_trials": 10,
                   "ibi_time": 10,
                   "variable_isi": True,
                   "name": "stroop_defaults"
                   }


finger_tapping_defaults = {
                           "num_blocks": 6,
                           "block_len_time": 15,
                           "ibi_time": 15,
                           "is_sound": False,
                           "name": "finger_tapping_defaults",
                           }
}

defaults_dicts = [stroop_defaults, finger_tapping_defaults]

for defaults in defaults_dicts:
    fname = defaults.pop("name")
    print(fname)
    pickle.dump(defaults, open(f"./saved_defaults/{fname}.pkl", "wb"))
