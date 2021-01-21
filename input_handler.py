from psychopy import core, event

class InputHandler(object):
    def __init__(self, mode="mri"):
        self.mode = mode
        self.mouse = event.Mouse()

        if mode == "mri":
            self.response_key_dict = {"default": ["1"],
                                      "response_1": ["1"],
                                      "response_2": ["2"],
                                      "response_all": ["1", "2"]}
            self.response_mouse_dict = {"left": 0,
                                        "middle": 1,
                                        "right": 2}
        else:
            self.response_key_dict = {"default": ["space"],
                                      "response_1": ["left"],
                                      "repsonse_2": ["right"],
                                      "response_all": ["left", "right"]}
            self.response_mouse_dict = {"left": 0,
                                        "middle": 1,
                                        "right": 2}


    def handle_button_input(self, input_key, timer=None):

        event.clearEvents()

        valid_keys = self.response_key_dict[input_key]
        if timer:
            while not event.getKeys(valid_keys) and not timer.getTime() < 0:
                continue
            if timer.getTime() > 0:
                return True
            return False
        else:
            while not event.getKeys(valid_keys):
                continue
            return True


    def handle_mouse_input(self, input_btn, timer=None):

        event.clearEvents()
        m_down = False

        core.wait(.15)

        # Wait till Mouse Press is UP.
        if timer:
            while not timer.getTime() < 0:
                if self.mouse.getPressed()[self.response_mouse_dict[input_btn]] == 1:
                    m_down = True
                if m_down and self.mouse.getPressed()[self.response_mouse_dict[input_btn]] == 0:
                    break
        else:
            while True:
                if self.mouse.getPressed()[self.response_mouse_dict[input_btn]] == 1:
                    m_down = True
                if m_down and self.mouse.getPressed()[self.response_mouse_dict[input_btn]] == 0:
                    break
