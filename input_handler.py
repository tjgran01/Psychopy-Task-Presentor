from psychopy import event

class InputHandler(object):
    def __init__(self, mode="mri"):
        self.mode = mode

        if mode == "mri":
            self.response_key_dict = {"default": ["1"],
                                      "response_1": ["1"],
                                      "response_2": ["2"],
                                      "response_all": ["1", "2"]}
        else:
            self.response_key_dict = {"default": ["space"],
                                      "response_1": ["left"],
                                      "repsonse_2": ["right"],
                                      "response_all": ["left", "right"]}


    def handle_button_input(self, input_key, timer=None):

        event.clearEvents()

        valid_keys = self.response_key_dict[input_key]
        if timer:
            while not event.getKeys(valid_keys) and not timer.getTime() < 0:
                continue
        else:
            while not event.getKeys(valid_keys):
                continue
