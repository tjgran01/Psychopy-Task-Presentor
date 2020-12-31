### Psychopy Stroop

#### Installing

1. Clone this repo.
2. Make a python environment `python3.6 -m venv venv`
3. Activate environment `source venv/bin/activate`
4. Install requirements `pip install -r requirements.txt`
5. run `python ./scripts/main.py`

#### Data

Data should be exported into `./data/{id_number}_{year}_{month}_{day}.csv`

#### Changing Parameters.

Most of the parameters of interest can be changed in the `stroop.py` file. They exist as keyword arguments. The current config is here for testing purposes.

Parameters can also be changed by linking them with a subject_id and entering them into a row in the `./preferences/id_preferences_table.csv`

```
num_blocks=2, fixation_time=2, congruence_rate=.2, num_trials=10, ibi_time=10
```

#### Big Picture Questions

1. How many pages of text **per block**?
2. How many questions in total? (per block)
3. How many mind wander probes? (if we aren't just doing it after whole block of reading...?)

Default assumption is page_num = question = mind wander probe?

csv or tsv |sv

page_text | page number | question text | answer text. | 0_1

#### Where to put things.

Texts:
  - `./resources/affect_reading_texts`
Video:
    `./resources/affect_reading_texts`
Question files:
    `./resources/affect_reading_questions`
Scale information:
    ``
