### Add this to end of slider.py in ./venv/lib/site-packages/psychopy/visual/

if 'myRadio' in style:

    # no line, ticks are circles
    self.line.opacity = 0
    # ticks are circles
    self.tickLines.sizes = (self._tickL, self._tickL)
    self.tickLines.elementMask = 'circle'
    # marker must be smalle than a "tick" circle
    self.marker.size = self._tickL * 0.7
    self.marker.color = "black"
    self.marker.fillColor = "black"
    for label in self.labelObjs:
        label.alignText = 'left'
