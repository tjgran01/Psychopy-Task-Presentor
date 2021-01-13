# Set up window and scale
from psychopy import visual
win = visual.Window()
scale = visual.RatingScale(win,
    labels=['Not at all confident', 'Extremely confident'],   # End points
    scale=None,  # Suppress default
    low=1, high=100, tickHeight=0)

# Show scale
while scale.noResponse:
    scale.draw()
    win.flip()

# Show response
print(scale.getRating(), scale.getRT())
