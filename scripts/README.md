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

**Fixation time is an ISI. I'll need to add a function to make it variable.**

```
num_blocks=2, fixation_time=2, congruence_rate=.2, num_trials=10, ibi_time=10
```
