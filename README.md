# Psychopy Stroop

## Installing

1. Clone this repository.
2. Make a python environment in root directory (folder where you are reading this from :)) `python3.8 -m venv venv`
3. Activate environment: `source venv/bin/activate`
4. Install requirements: `pip install -r requirements.txt`
5. run `python ./scripts/main.py`
6. To leave the enviornment you can just exit the terminal. or type `deactivate`.

***Note:*** You may get some errors while install requirements. The most common one is wxPython.

Try:

`pip install wxPython` and then rerun `pip install -r requirements.txt`.

If wxPython is still giving you trouble. Check [here](https://www.wxpython.org/pages/downloads/) for the wheel files, or further info.

## Notes on running.

### Inputs.

#### "Waiting for Scanner Event":

Press "5" on the keyboard to advance.

#### Stroop and Finger Tapping.

`stroop` and `finger_tapping` are expecting button box inputs. As such "Index Finger Button" refers to "1" on the keyboard. "Middle Finger Button" refers to "1" on the keyboard.

#### Affect Reading.

`Affect Reading` are expecting trackball inputs. Therefore use the mouse. "Index finger Button" refers to a LEFT CLICK. "Scroll Left/Right" mean move mouse left right. "Scroll Up/Down" means move mouse up and down.

### Editing task order.

If you want to just run one task on into `main.py` and edit the `task_list` variable. (Line 24 as of 1/29/20).

Always make sure the task list ends with `"end"`.

Acceptable parameters are:

`"stroop"`, `"affect_reading"`, `"finger_tapping"`, `"end"`

### Editing task parameters.

Many optional parameters for tasks can be changed via the `./create_default_params_files.py` script.

The parameters in this file are stored in dictionaries corresponding to their respective tasks. i.e. `finger_tapping_defaults`.

If you wish to edit one of these parameters change it in this file and then **RERUN** the script. This will serialize this data so the next time you run the main application, it will pull from the edits you've made.

Most of the variable names in the file should make sense.

#### Notes on `affect_reading`:

1. Testing Mode.

This task is a bit of a bear. There is a variable in `create_default_params_files.py` that allows for a testing mode. This will bypass the typical block design and allow you to customize what you want to run by calling the methods in the last method listed in the `affect_reading.py` file: `run_test(self)`. Set `testing` to `True`.

2. Fixation padding.

Because this task will be run in an MRI scanner. Fixations will need to be padded in order to ensure the task is run at the proper length. This is a nightmare for testing. So there is an option to remove these paddings in the `create_default_params_files.py` file. Set `use_padding` to `False`.

##### NOTE:

ISI = Inner Stimulus Interval and refers to a fixation between presentations of a task (i.e. a trial).

IBI = Inner Block Interval and refers to a fixation between presentations of a block (i.e. a SET of trials.)



## TODOs

~1. Change background to black with slightly grey font color.~

~2. Make Sliders continuous as opposed to discrete.~

~3. Create new Input_Handler to work with button box~

~3. ... and trackball. (1,2) for index / middle.~

~4. Set Pages that wait for TTL from MRI (5)~

~5. Add timeouts to questions.~

~6. Definitely need a refactor :)~

7. Link up triggers for all stim.

8. Write a TTL Pulse class for EEG trig.

~9. Look into connecting EyeLink. I need some information on this.~

~10. Make Stroop use congruence rather than color choice.~

~11. Finger tapping - add response logging.~

~12. Add slider practice.~

~13. Pad times for fMRI.~

~14. Change to sentence level presentation. Self paced. Hard timeout.~


## Exported Data

Data should be exported into `./data/{task}/{id_number}_{year}_{month}_{day}.csv`

Data is recorded to these files as it is generated. i.e. If the application quits early you will still have a record of all of the data up until the point at which the application quit.

## Where to put things.

### Affect Reading.

Texts:
  - `./resources/affect_reading_texts`

Video:
    `./resources/affect_videos`

Question files:
    `./resources/affect_reading_questions`

### TODO:

1. Add practice mode for conditions. DONE
2. Want a break every 14 trials. 30 Sec break.
3. 2 breaks total.
4. last block with only have 12 trials.
5. Same condition the whole time.
6. Randomly select 7 / 7, 7 / 7, 6 / 6 of each condition in each "Block".
