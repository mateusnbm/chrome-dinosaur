#
# dino_main.py
#


import sys
import time

from pymouse import PyMouse
from pykeyboard import PyKeyboard

import dino.scanner
import dino.sensors


'''
Initialization.
'''

mouse = PyMouse()
keyboard = PyKeyboard()

game_rect = dino.scanner.findGameBoundaries()
game_screenshot = dino.scanner.capture_screenshot(game_rect)
dino_rect = dino.scanner.findDino(game_screenshot)

#dino.sensors.draw_sensors(game_screenshot, dino_rect)
#exit(0)

'''
Main program loop.
'''

while(1):

    input("\nPress enter to start a new game...")

    # Place the cursor above Google Chrome and click twice, one to make it
    # the active window and the second to start the game.

    x = game_rect[0][0] + 15
    y = game_rect[0][1] + game_rect[1][1] - 20

    mouse.click(x, y)
    mouse.click(x, y)

    # Wait 100 ms to avoid detecting the game over sign from a previous game.

    time.sleep(0.1)

    # Game loop. Capture a screenshot every 5 ms and analyse it to determine
    # the game state, update enemies information and to control the dinosaur.

    sensor_data = None
    jumps_count = 0
    genome_index = 0

    while(1):

        # Delay iteration by 5 ms. This delay is placed at the begining of the
        # loop because it will be more convenient to use 'continue' statements
        # to skip loop iterations.

        time.sleep(0.005)

        # Capture screenshot, terminate if the game over screen is detected.

        game_screenshot = dino.scanner.capture_screenshot(game_rect)

        if dino.scanner.game_over(game_screenshot) == True:

            break

        # Read sensors information.

        read, jumped, sensor_data = dino.sensors.read(game_screenshot, dino_rect, sensor_data)

        if jumped == True: jumps_count += 1
        if read == False: continue

        distance = sensor_data[0]
        size = sensor_data[1]
        speed = sensor_data[2]

        # Display the updated metrics.

        print("")
        print("Distance: " + str(distance))
        print("Size: " + str(size))
        print("Speed: " + str(speed))
        print("Activation: " + str(0))

    print("")
    print("Tested genome 0/10, fitness " + str(jumps_count) + ".")

    # Place the cursor above the terminal window to make it the active one.

    w, h = mouse.screen_size()

    x = w * 0.8
    y = h * 0.5

    mouse.click(x, y)

'''
'''

# ...
