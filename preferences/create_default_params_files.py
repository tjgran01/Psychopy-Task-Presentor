import pickle

#### EDIT THIS TO EDIT DEFAULT PARAMETERS.

stroop_defaults = {
                   "num_blocks": 10,
                   "fixation_time": 2, # How long between trials.
                   "congruence_rate": .5,
                   "num_trials": 20,
                   "ibi_time": 10,
                   "variable_isi": True, # Will use 'fixation_time as mean.'
                   "scoring_method": "congruence",
                   "response_timeout": 5,
                   "name": "stroop_defaults",
                   }


finger_tapping_defaults = {
                           "num_blocks": 12,
                           "block_time": 24, # In seconds
                           "ibi_time": 16, # In seconds
                           "is_sound": False,
                           "tap_window": .250, # in seconds.
                           "conditions": [[120, "left"],
                                          [80, "left"],
                                          [120, "both"],
                                          [80, "both"],
                                          [120, "right"],
                                          [80, "right"],
                                          [120, "left"],
                                          [80, "left"],
                                          [120, "both"],
                                          [80, "both"]],
                           "name": "finger_tapping_defaults",
                           }


affect_reading_defaults = {
                           "num_blocks": 2,
                           "affect_order": ["none", "happy"],
                           "max_reading_time": 150,
                           "readings": ["hypotheses", "causalclaims"],
                           "mult_choice_question_num": 4,
                           "question_mode": "likert",
                           "text_size_mult": 0.7,
                           "randomize_mult_choice_presentation": True,
                           "snap_questions": False,
                           "randomize_question_presentation": True,
                           "movie_size_mult": 2.5,
                           "affect_induction_time": 150, # in seconds.
                           "name": "affect_reading_defaults"
                           }

defaults_dicts = [stroop_defaults, finger_tapping_defaults, affect_reading_defaults]

for defaults in defaults_dicts:
    fname = defaults.pop("name")
    pickle.dump(defaults, open(f"./saved_defaults/{fname}.pkl", "wb"))
