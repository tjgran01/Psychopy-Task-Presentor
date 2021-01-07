from psychopy import visual, core

from parameters.trigger_dict import trigger_dict, trigger_string_dict

class FingerTappingTask(object):
    def __init__(self, sub_id, task_presentor, num_blocks=6, block_time=15, ibi_time=15,
                 is_sound=False):
        self.task_name = "finger_tapping"
        self.sub_id = sub_id
        self.task_presentor = task_presentor
        self.num_blocks = num_blocks
        self.block_time = block_time
        self.ibi_time = ibi_time
        self.is_sound = is_sound

        self.conditions_list = [
                                 [120, "right"],
                                 [80, "right"],
                                 [120, "left"],
                                 [80, "left"],
                                 [120, "both"],
                                 [80, "both"],
                               ]

        if is_sound:

            from psychopy.sound import Sound

            self.sound = Sound(value="C", secs=0.05, octave=4)
            self.follow_sound = Sound(value="G", secs=0.05, octave=4)
            self.sound_list = [self.sound, self.follow_sound, self.follow_sound, self.follow_sound]
            self.beat_count = 0
            self.instructions = self.task_presentor.read_instructions_from_file(self.task_name)
        else:
            self.instructions = self.task_presentor.read_instructions_from_file(f"{self.task_name}_no_sound")


    def run_full_task(self):

        self.task_presentor.display_instructions(self.instructions)

        for block in range(self.num_blocks):
            self.run_block(block_num=block, bpm=self.conditions_list[block][0], hand_condition=self.conditions_list[block][1])
            self.task_presentor.run_ibi(self.ibi_time)

        self.export_data()


    def run_block(self, bpm, hand_condition, block_num=0):

        trigger_int = self.determine_trigger_int(bpm, hand_condition)

        tap_text = visual.TextStim(self.task_presentor.window, text="TAP")
        if hand_condition == "both":
            top_text = visual.TextStim(self.task_presentor.window, text=f"TAP {hand_condition.upper()} INDEX FINGERS IN TIME WITH THE BEAT", pos=(0.0, 0.8))
        else:
            top_text = visual.TextStim(self.task_presentor.window, text=f"TAP {hand_condition.upper()} INDEX FINGER IN TIME WITH THE BEAT", pos=(0.0, 0.8))

        trial_timer = core.CountdownTimer(60.0 / bpm)
        block_timer = core.CountdownTimer(self.block_time)

        self.display_condition_prompt(condition_string=hand_condition)

        top_text.draw()
        self.task_presentor.window.flip()

        core.wait(.1)
        self.task_presentor.trigger_handler.send_int_trigger(trigger_int)
        block_timer.reset()
        
        while block_timer.getTime() > 0:
            current_time = str(int(block_timer.getTime()))
            timer_text = visual.TextStim(self.task_presentor.window, text=current_time, pos=(-0.9, 0.9))
            while trial_timer.getTime() > 0:
                pass
            trial_timer.reset()
            if self.is_sound:
                self.sound_list[self.beat_count].play()
                self.beat_count+=1
                if self.beat_count > 3:
                    self.beat_count = 0
            top_text.draw()
            tap_text.draw()
            timer_text.draw()
            self.task_presentor.window.flip()
            core.wait(0.2)
            self.task_presentor.fixation_cross.draw()
            top_text.draw()
            timer_text.draw()
            self.task_presentor.window.flip()
            if self.is_sound:
                self.sound_list[self.beat_count].stop()

        # 3 means task ended.
        self.task_presentor.trigger_handler.send_int_trigger(trigger_string_dict["Task_End"])
        core.wait(.2)
        return


    def run_condition(self, hand_condition, bpm, total_time=60):

        start_sound = sound.Sound("C", secs=0.1, octave=5)
        after_sound = sound.Sound("G", secs=0.1, octave=4)

        timer = core.CountdownTimer(total_time)
        while time.getTime() > 0:
            pass


    def determine_trigger_int(self, bpm, hand_condition):

        return trigger_string_dict[f"Finger_Tapping_{hand_condition}_{bpm}"]


    def display_condition_prompt(self, condition_string=""):

        if condition_string == "both":
            added_s = "s"
        else:
            added_s = ""

        to_draw = [
                   self.task_presentor.advance_text,
                   visual.TextStim(self.task_presentor.window, text=f"For this condition you will be tapping your {condition_string.upper()} hand.")
                  ]

        self.task_presentor.draw_and_wait_for_input(what_to_draw=to_draw)


    def export_data(self):
        pass