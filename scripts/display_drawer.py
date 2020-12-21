from psychopy import visual

class DisplayDrawer(object):
    """
    Class that draws objects to screen. DOES NOT FLIP WINDOW.
    The main method by which this works is by adding all elements that
    need to be drawn to self.draw_list, and then drawing them all.
    window.flip() should still be called within the main program, or
    the object that is calling the display drawer.
    Args:
        None
    Returns:
        None.
    """
    def __init__(self, draw_list=[]):
        self.draw_list = draw_list
        self.last_draw = []


    def add_to_draw_list(self, elm):
        self.draw_list.append(elm)


    def remove_from_draw_list(self, elm):
        self.draw_list.remove(elm)


    def draw_all(self):
        [elm.draw() for elm in self.draw_list]
        self.shelf_last_draw(self.draw_list)
        self.flush_all()


    def flush_all(self):
        self.draw_list = []


    def shelf_last_draw(self, last_draw):
        self.last_draw = last_draw


    def flush_last_draw(self):
        self.last_draw = []
