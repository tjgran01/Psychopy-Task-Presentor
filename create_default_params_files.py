import pickle

#### EDIT THIS TO EDIT DEFAULT PARAMETERS.

def set_defaults():

    for defaults in defaults_dicts:
        fname = defaults.pop("name")
        pickle.dump(defaults, open(f"./preferences/saved_defaults/{fname}.pkl", "wb"))

stroop_defaults = {
                   "num_blocks": 6,
                   "fixation_time": 2, # How long between trials.
                   "conditions": ["congruent",
                                  "incongruent",
                                  "congruent",
                                  "incongruent",
                                  "congruent",
                                  "incongruent"],
                   "congruence_rate_congruent": 1,
                   "congruence_rate_incongruent": .33,
                   "num_trials": 20, # overridden if block_time != 0.
                   "ibi_time": 15,
                   "variable_isi": False, # Will use 'fixation_time as mean.'
                   "scoring_method": "congruence",
                   "response_timeout": 5,
                   "block_time": 30,
                   "shuffle_conditions": True,
                   "name": "stroop_defaults",
                   }


finger_tapping_defaults = {
                           "num_blocks": 6,
                           "block_time": 15, # In seconds
                           "ibi_time": 10, # In seconds
                           "is_sound": False,
                           "tap_window": .250, # in seconds.
                           "conditions": [[80, "right"],
                                          [80, "right"],
                                          [80, "right"],
                                          [80, "right"],
                                          [80, "right"],
                                          [80, "right"]],
                           "name": "finger_tapping_defaults",
                           }


affect_reading_defaults = {
                           "num_blocks": 2,
                           "affect_order": ["none", "sad"],
                           "max_reading_time": 150,
                           "readings": {"A":["validity", "variables"],
                                        "B": ["causalclaims", "hypotheses"]},
                           "mult_choice_question_num": 3,
                           "question_mode": "likert",
                           "text_size_mult": 1,
                           "randomize_mult_choice_presentation": True,
                           "snap_questions": False,
                           "randomize_question_presentation": True,
                           "movie_size_mult": .7,
                           "affect_induction_time": 150, # in seconds.
                           "default_fixation_time": 2,
                           "question_timeouts": {"slider alert": 10,
                                                 "slider affect": 10,
                                                 "slider mind_wandering": 10,
                                                 "slider mult_choice": 22,
                                                 "slider practice_slider": 30,
                                                 "slider practice_mult_choice": 30},
                           "testing": False,
                           "use_padding": True,
                           "video_text_timer_prompt": 3,
                           "reading_text_timer_prompt": 3,
                           "name": "affect_reading_defaults"
                           }

emotional_anticipation_defaults = {
                                   "num_blocks": 1,# Not used since there is only one block.
                                   "ibi_time": 30, # Not used since there is only one block. REST TIME.
                                   "fixation_time": 6.9, # How long between cue and stim.
                                   "iti_time": 3, # Time between individual stimulus presentations
                                   "cue_time": 1, # How long cue stays on screen.
                                   "video_sub_cue_time": 2,# how long a cue is displayed if it is not a video.
                                   "movie_time": 6.9, # How long the video plays
                                   "num_trials": 96, # overridden if block_time != 0. PROBABLY UNUSED CURRENTLY.
                                   "variable_isi": False, # Will use 'fixation_time as mean.'
                                   "question_timeouts": {"slider affect": 4},
                                   "conditions": ["darker",
                                                  "lighter"],
                                   "name": "emotional_anticipation_defaults",
                                   }

episodic_prospection_defaults = {
                                  "num_blocks": 1,
                                  "ibi_time": 15,
                                  "fixation_time": 2, # How long between cue and stim.
                                  "cue_time": 15, # How long the word is played for.
                                  "iti_time": 6, # Time between individual stimulus presentations
                                  "num_trials": 40, # overridden if block_time != 0. PROBABLY UNUSED CURRENTLY.
                                  "variable_isi": False, # Will use 'fixation_time as mean.'
                                  "name": "episodic_prospection_defaults",
                                  "question_timeouts": {"slider affect": 4},
                                  "conditions": ["None"]
}

social_self_control_defaults = {
                                "num_blocks": 1,
                                "ibi_time": 0,
                                "fixation_time": 2, # How long between cue and stim.
                                "cue_time": 2, # How long the word is played for.
                                "iti_time": 6, # Time between individual stimulus presentations
                                "num_trials": 64, # overridden if block_time != 0. PROBABLY UNUSED CURRENTLY.
                                "variable_isi": True, # Will use 'fixation_time as mean.'
                                "stim_time": 10,
                                "name": "social_self_control_defaults",
                                "question_timeouts": {"slider affect": 4},
                                "conditions": ["None"],
                                "is_non_social": False
}

non_social_self_control_defaults = {
                                    "num_blocks": 1,
                                    "ibi_time": 0,
                                    "fixation_time": 2, # How long between cue and stim.
                                    "cue_time": 2, # How long the word is played for.
                                    "iti_time": 6, # Time between individual stimulus presentations
                                    "num_trials": 64, # overridden if block_time != 0. PROBABLY UNUSED CURRENTLY.
                                    "variable_isi": True, # Will use 'fixation_time as mean.',
                                    "stim_time": 20,
                                    "name": "non_social_self_control_defaults",
                                    "question_timeouts": {"slider affect": 4},
                                    "conditions": ["None"],
                                    "is_non_social": True # Shows whether this is a non-social task.
}

defaults_dicts = [stroop_defaults,
                  finger_tapping_defaults,
                  affect_reading_defaults,
                  emotional_anticipation_defaults,
                  episodic_prospection_defaults,
                  social_self_control_defaults,
                  non_social_self_control_defaults]



if __name__ == "__main__":
    set_defaults()
