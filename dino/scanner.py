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

game_over_letter_m_x = 537
game_over_letter_m_y = 83
game_over_letter_v_x = 704
game_over_letter_v_y = 83
game_over_letter_colors = [82, 83, 84]


'''
Captures a screenshot of the given rect and returns a PIL Image object.
'''

def capture_screenshot(rect):

    x = rect[0][0]
    y = rect[0][1]
    w = rect[1][0]
    h = rect[1][1]

    monitor_rect = {'left': x, 'top': y, 'width': w, 'height': h}

    sct = mss.mss()
    sct_img = sct.grab(monitor_rect)
    pil_img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

    return pil_img


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

    x = x0 - game_window_left_padding
    y = y0 - game_window_top_padding
    w = xn - x0 + game_window_left_padding + game_window_right_padding
    h = game_window_top_padding + game_window_bottom_padding

    bounding_box = ((x, y), (w, h))

    # Draw a rectangle over the captured screen showing the inferred bounding
    # box, this is helpful while debugging the application.

    xn = bounding_box[0][0]+bounding_box[1][0]
    yn = bounding_box[0][1]+bounding_box[1][1]

    draw = ImageDraw.Draw(image)
    draw.rectangle(((x, y), (xn, yn)), outline="red")
    image.save('configuration/game_bounding_box.png')

    # It is necessary to adjust the bounding box in case this program is
    # running on a computer with retina display (@2x), to account for the
    # doubled screenshot size.

    if retina_monitor == True:

        x = bounding_box[0][0]/2
        y = bounding_box[0][1]/2
        w = bounding_box[1][0]/2
        h = bounding_box[1][1]/2

        bounding_box = ((x, y), (w, h))

    return bounding_box


'''
Find the dinosaur and computes an approximated bounding box.
'''

def findDino(game_screenshot):

    lock0 = False
    x0 = y0 = 0

    # Load the image so we can iterate through the pixels looking for the
    # left-most pixel of the dino (its tail).

    image_pixels = game_screenshot.load()
    width, height = game_screenshot.size

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

    draw = ImageDraw.Draw(game_screenshot)
    draw.rectangle(((x0, y0), (xn, yn)), outline="purple")
    game_screenshot.save("configuration/dinos_bounding_box.png")

    return bounding_box


'''
Determines if the game over screen is visible in the given frame.
'''

def game_over(game_screenshot):

    pixels = game_screenshot.load()

    # Check the position of the first pixels that compose the letters M and V
    # from the game over sign to see if they match the dinosaur color.

    m = pixels[game_over_letter_m_x, game_over_letter_m_y][0]
    v = pixels[game_over_letter_v_x, game_over_letter_v_y][0]

    return (m in game_over_letter_colors) and (v in game_over_letter_colors)
