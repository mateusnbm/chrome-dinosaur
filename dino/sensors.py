#
# sensors.py
#


import time
import datetime

from PIL import Image, ImageDraw


'''
Parameters.
'''

enemies_colors = [83, 84]

sensor_bars_count = 40
sensor_bars_length = 180
sensor_bars_padding = 10
sensor_bars_left_margin = 10
sensor_bars_bottom_margin = 35

enemy_lookout_left = 30
enemy_lookout_top = 10
enemy_lookout_right = 120
enemy_lookout_bottom = 10


'''
Draw vertical bars showing the portion of the screen that the sensor analyse.
'''

def draw_sensors(game_screenshot, dino_rect):

    dino_xn = dino_rect[0][0] + dino_rect[1][0]
    dino_yn = dino_rect[0][1] + dino_rect[1][1]

    base_x = dino_xn + sensor_bars_left_margin
    base_y = dino_yn - sensor_bars_length - sensor_bars_bottom_margin

    image_pixels = game_screenshot.load()
    draw = ImageDraw.Draw(game_screenshot)

    for i in range(sensor_bars_count):

        x0 = base_x
        y0 = base_y
        xn = base_x
        yn = y0 + sensor_bars_length

        base_x += sensor_bars_padding

        draw.rectangle(((x0, y0), (xn, yn)), outline="green")

    game_screenshot.save("configuration/sensor_bars.png")


'''
Checks each sensor bar (left to right) looking for a pixels matching
the enemies color. Returns the position or -1 to indicate no matches.
'''

def find_enemy(pixels, bars_base_x, bars_base_y):

    enemy_x = -1
    enemy_y = -1

    i = 0
    x = bars_base_x

    while i < sensor_bars_count:

        j = 0
        y = bars_base_y

        while j < sensor_bars_length:

            if pixels[x, y][0] in enemies_colors:

                i = sensor_bars_count
                j = sensor_bars_length

                enemy_x = x
                enemy_y = y

            j += 1
            y += 1

        i += 1
        x += sensor_bars_padding

    return enemy_x, enemy_y


'''
'''

def find_enemy_bounding_box(pixels, enemy_x, enemy_y):

    x_min = x_max = enemy_x
    y_min = y_max = enemy_y

    x = enemy_x - enemy_lookout_left
    y = enemy_y - enemy_lookout_top
    w = enemy_x + enemy_lookout_right - x
    h = enemy_y + enemy_lookout_bottom - y

    for i in range(w):

        for j in range(h):

            if pixels[x+i, y+j][0] in enemies_colors:

                if (x+i) < x_min: x_min = (x+i)
                if (x+i) > x_max: x_max = (x+i)

                if (y+j) < y_min: y_min = (y+j)
                if (y+j) > y_max: y_max = (y+j)

    return ((x_min, y_min), (x_max-x_min, y_max-y_min))


'''
'''

def read(game_screenshot, dino_rect, previous_sensor_data):

    pixels = game_screenshot.load()

    # Calculate the starting point of the left-most bar.

    dino_xn = dino_rect[0][0] + dino_rect[1][0]
    dino_yn = dino_rect[0][1] + dino_rect[1][1]

    base_x = dino_xn + sensor_bars_left_margin
    base_y = dino_yn - sensor_bars_length - sensor_bars_bottom_margin

    # Iterate through the bars looking for a pixel matching the enemies
    # color. If none was found, there is nothing else to do in here.

    enemy_x, enemy_y = find_enemy(pixels, base_x, base_y)

    if enemy_x == -1:

        return False, False, previous_sensor_data

    # An enemy was detected, lets compute its bounding box.

    bounding_box = find_enemy_bounding_box(pixels, enemy_x, enemy_y)

    # Check if the enemy is about to reach the same horizontal coordinate of
    # the dinosaur, if so, we no longer need to track it.

    if bounding_box[0][0] <= (dino_xn + (enemy_lookout_left/2)):

        return False, False, previous_sensor_data

    # Check if the sensor detected a new enemy, if so, the dinosaur already
    # jumped the previous one, then, we report the jump.

    jumped = False

    if previous_sensor_data is not None:

        if bounding_box[0][0] - previous_sensor_data[3][0][0] > 100:

            jumped = True
            previous_sensor_data = None

    # Compute the enemy's distance, size and speed. The size will always be
    # equal to the first measured size (appears to be the most precise). In
    # order to measure the speed, we need to have previous measurements, so,
    # once a valid 'previous_sensor_data' is given, we can determine the speed.

    distance = bounding_box[0][0] - dino_xn

    if previous_sensor_data is None:

        size = bounding_box[1][0]

        speed = -1
        speeds = []
        time_ms = time.time()/1000

    else:

        size = previous_sensor_data[1]

        time_ms = time.time()/1000
        time_ms_delta = previous_sensor_data[4]

        previous_x = previous_sensor_data[3][0][0]
        current_x = bounding_box[0][0]
        current_speed = (previous_x - current_x) / time_ms_delta

        speeds = previous_sensor_data[5]
        speeds.append(current_speed)

        previous_speed = previous_sensor_data[2]
        avg_speed = sum(speeds) / len(speeds)
        speed = max(previous_speed, avg_speed)

    # Return the enemy's distance, size, speed and some other stuff.

    return True, jumped, [distance, size, speed, bounding_box, time_ms, speeds]
