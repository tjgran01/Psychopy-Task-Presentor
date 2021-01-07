import pickle

#### EDIT THIS TO EDIT DEFAULT PARAMETERS.

stroop_defaults = {
                   "num_blocks": 10,
                   "fixation_time": 2,
                   "congruence_rate": .2,
                   "num_trials": 20,
                   "ibi_time": 10,
                   "variable_isi": True,
                   "name": "stroop_defaults"
                   }


finger_tapping_defaults = {
                           "num_blocks": 12,
                           "block_time": 15, # In seconds
                           "ibi_time": 15, # In seconds
                           "is_sound": False,
                           "name": "finger_tapping_defaults",
                           }


affect_reading_defaults = {
                           "num_blocks": 2,
                           "affect_order": ["none", "happy"],
                           "max_reading_time": 150,
                           "readings": ["hypotheses", "causalclaims"],
                           "mult_choice_question_num": 4,
                           "name": "affect_reading_defaults"
                           }

defaults_dicts = [stroop_defaults, finger_tapping_defaults, affect_reading_defaults]

for defaults in defaults_dicts:
    fname = defaults.pop("name")
    pickle.dump(defaults, open(f"./saved_defaults/{fname}.pkl", "wb"))
