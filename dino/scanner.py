#
# dino_scanner.py
#


import mss
import mss.tools

from PIL import Image, ImageDraw


'''
Parameters.
'''

retina_monitor = True

dino_color = 83
dino_max_width = 110
dino_max_height = 86

game_window_left_padding = 30
game_window_top_padding = 260
game_window_right_padding = 30
game_window_bottom_padding = 30


'''
Finds the game from a screenshot and computes an approximated bounding box.
'''

def findGameBoundaries():

    lock0 = lockn = False
    x0 = y0 = xn = yn = 0

    # Grab screenshot using MSS (allegedly faster than PIL).

    sct = mss.mss()
    sct_img = sct.grab(sct.monitors[1])

    # Load the image so we can iterate through the pixels looking for the
    # left-most pixel of the ground (bottom line, same color as the dinosaur).

    image = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
    image_pixels = image.load()
    width, height = image.size

    for x in range(width):

        for y in range(height):

            l0 = image_pixels[x, height-y-1][0]
            ln = image_pixels[width-x-1, height-y-1][0]

            # Look for the left-most pixel of the bottom line (the ground).

            if  lock0 == False and l0 == dino_color:

                x0 = x
                y0 = height-y-1
                lock0 = True

            # Look for the right-most pixel of the bottom line (the ground).

            if  lockn == False and ln == dino_color:

                xn = width-x-1
                yn = height-y-1
                lockn = True

    # Compute the game bounding box. This will determine the portion of the
    # screen that we analyse in each iteration of our controller.

    x0 = (x0 - game_window_left_padding)
    y0 = (y0 - game_window_top_padding)
    width = (xn - x0 + game_window_left_padding + game_window_right_padding)
    height = (game_window_top_padding + game_window_bottom_padding)

    bounding_box = ((x0, y0), (width, height))

    # Draw a rectangle over the captured screen showing the inferred bounding
    # box, this is helpful while debugging the application.

    xn = bounding_box[0][0]+bounding_box[1][0]
    yn = bounding_box[0][1]+bounding_box[1][1]

    draw = ImageDraw.Draw(image)
    draw.rectangle(((x0, y0), (xn, yn)), outline="red")
    image.save('configuration/game_bounding_box.png')

    return bounding_box


'''
Find the dinosaur and computes an approximated bounding box.
'''

def findDino(game_rect):

    lock0 = False
    x0 = y0 = 0

    # Capture the portion of the screen that contains the game, so, we restrain
    # the search area to a smaller portion of the screen.

    monitor_rect = {
        'top': game_rect[0][1],
        'left': game_rect[0][0],
        'width': game_rect[1][0],
        'height': game_rect[1][1],
        }

    if retina_monitor == True:

        # It is necessary to make this adjustment in retina displays (@2x)
        # since MSS stipulates monitor coordinates in standard resolution (@1x).

        monitor_rect['top'] /= 2
        monitor_rect['left'] /= 2
        monitor_rect['width'] /= 2
        monitor_rect['height'] /= 2

    sct = mss.mss()
    sct_img = sct.grab(monitor_rect)

    # Load the image so we can iterate through the pixels looking for the
    # left-most pixel of the dino (its tail).

    image = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
    image_pixels = image.load()
    width, height = image.size

    for x in range(100):

        for y in range(height-50):

            if  lock0 == False and image_pixels[x, y][0] == dino_color:

                x0 = x
                y0 = y
                lock0 = True

    # Compute the dino's bounding box.

    x0 = (x0 - 0)
    y0 = (y0 - 30)
    width = dino_max_width
    height = dino_max_height

    bounding_box = ((x0, y0), (width, height))

    # Draw a rectangle over the captured screen to highlight the dino's
    # bounding box, this is helpful while debugging the application.

    xn = bounding_box[0][0]+bounding_box[1][0]
    yn = bounding_box[0][1]+bounding_box[1][1]

    draw = ImageDraw.Draw(image)
    draw.rectangle(((x0, y0), (xn, yn)), outline="purple")
    image.save("configuration/dinos_bounding_box.png")

    return bounding_box
