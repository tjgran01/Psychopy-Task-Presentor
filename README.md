### Psychopy Stroop

#### Installing

1. Clone this repository.
2. Make a python environment in root directory (folder where you are reading this from :)) `python3.8 -m venv venv`
3. Activate environment `source venv/bin/activate`
4. Install requirements `pip install -r requirements.txt`
5. run `python ./scripts/main.py`

####

TODO

~1. Change background to black with slightly grey font color.~

2. Make Sliders continuous as opposed to discrete.
3. Create new Input_Handler to work with button box and trackball. (1,2) for index / middle.

~4. Set Pages that wait for TTL from MRI (5)~

~5. Add timeouts to questions.~

~6. Definitely need a refactor :)~

7. Link up triggers for all stim.
8. Write a TTL Pulse class for EEG trig.
9. Look into connecting EyeLink. I need some information on this.


#### Data

Data should be exported into `./data/{task}/{id_number}_{year}_{month}_{day}.csv`

#### Changing Parameters.

Most of the parameters of interest can be changed in the `stroop.py` file. They exist as keyword arguments. The current config is here for testing purposes.

Parameters can also be changed by linking them with a subject_id and entering them into a row in the `./preferences/id_preferences_table.csv`

```
num_blocks=2, fixation_time=2, congruence_rate=.2, num_trials=10, ibi_time=10
```

#### Where to put things.

##### Affect Reading.

Texts:
  - `./resources/affect_reading_texts`
Video:
    `./resources/affect_videos`
Question files:
    `./resources/affect_reading_questions`
