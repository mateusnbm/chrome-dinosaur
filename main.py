#
# dino_main.py
#


import sys
import time
import random
import datetime

from pymouse import PyMouse
from pykeyboard import PyKeyboard

import dino.scanner
import dino.sensors
import dino.conveniences

from dino.genetic import Genome
from dino.network import NeuronLayer, NeuralNetwork


'''
Initialization.
'''

mouse = PyMouse()
keyboard = PyKeyboard()

game_rect = dino.scanner.findGameBoundaries()
game_screenshot = dino.scanner.capture_screenshot(game_rect)
dino_rect = dino.scanner.findDino(game_screenshot)

fileid = str(int(time.time()) )
filename = "genomes/" + fileid + ".txt"
file = open(filename, 'w+')


'''
Artificial intelligence stuff.
'''

recombination_probability = 0.8
mutation_probability = 0.2

genomes_cut = 6
genomes_size = 32
genomes_count = 12
genomes_index = 0
genomes_generation = 1

#genomes = [Genome(length=genomes_size) for _ in range(genomes_count)]
genomes = dino.conveniences.load_genomes_from_file("genomes/1528251380.txt", genomes_count, genomes_size)

layer_1 = NeuronLayer(number_of_neurons=4, number_of_inputs_per_neuron=3)
layer_2 = NeuronLayer(number_of_neurons=4, number_of_inputs_per_neuron=4)
layer_3 = NeuronLayer(number_of_neurons=1, number_of_inputs_per_neuron=4)

neural_network = NeuralNetwork([layer_1, layer_2, layer_3])


'''
Main program loop.
'''

while(1):

    input("\nPress enter to start a new game...")

    sensor_data = None
    jumps_count = 0

    # Place the cursor above Google Chrome and click twice, one to make it
    # the active window and the second to start the game.

    x = game_rect[0][0] + 15
    y = game_rect[0][1] + game_rect[1][1] - 20

    mouse.click(x, y)
    mouse.click(x, y)

    # Load the current genome genes as the network weights.

    neural_network.load_weights_from_genome(genomes[genomes_index])

    # Wait 100 ms to avoid detecting the game over sign from a previous game.

    time.sleep(0.1)

    # Game loop. Capture a screenshot every 5 ms and analyse it to determine
    # the game state, update enemies information and to control the dinosaur.

    while(1):

        # Delay iteration by 5 ms. This delay is placed at the begining of the
        # loop because it will be more convenient to use 'continue' statements
        # to skip loop iterations.

        time.sleep(0.005)

        # Capture screenshot, terminate if the game over screen is detected.

        game_screenshot = dino.scanner.capture_screenshot(game_rect)

        if dino.scanner.game_over(game_screenshot) == True: break

        # Read sensors information.

        read, jumped, sensor_data = dino.sensors.read(game_screenshot, dino_rect, sensor_data)

        if jumped == True: jumps_count += 1
        if read == False: continue
        if sensor_data[2] == -1: continue

        distance = sensor_data[0]
        size = sensor_data[1]
        speed = sensor_data[2]

        # Run through the current genome network to determine the activation.

        activation = neural_network.think([distance, size, speed])

        # Control dinosaur.

        if activation > 0.55: keyboard.tap_key('space')

        # Display the updated metrics.

        print("")
        print("Distance: " + str(distance))
        print("Size: " + str(size))
        print("Speed: " + str(speed))
        print("Activation: " + str(activation))

    print("")
    print("Generation: " + str(genomes_generation))
    print("Genome " + str(genomes_index+1) + "/" + str(genomes_count) + ".")
    print("Fitness: " + str(jumps_count) + ".")

    # Update the genome's fitness, persist it and update the test index.

    genomes[genomes_index].add_fitness(jumps_count)
    file.write(str(genomes[genomes_index]) + "\n")
    genomes_index += 1

    # When all 12 genomes have been tested, we remove the 6 worst and run
    # recombinations/mutations to generate new 6 genomes, then, start the
    # cycle again.

    if genomes_index == genomes_count:

        # Sort genomes by their fitnesses and remove the worst.

        genomes = sorted(genomes, key=lambda x: x.get_fitness(), reverse=True)
        genomes = genomes[:genomes_cut]

        # Select parents, recombine, mutate childs and append to the genomes.

        for i in range(genomes_cut//2):

            a = random.choice(genomes)
            b = random.choice(genomes)

            c, d = a.recombine(b, recombination_probability)

            c.mutate(mutation_probability)
            d.mutate(mutation_probability)

            genomes.extend([c, d])

        # Update indexes.

        genomes_index = 0
        genomes_generation += 1

    # Place the cursor above the terminal window to make it the active one.

    w, h = mouse.screen_size()

    x = w * 0.8
    y = h * 0.5

    mouse.click(x, y)

    # Quick hack to keep executing the program multiple times, useful while
    # learning the best network parameters. Commend the lines below to wait
    # for a keypress after each execution.

    keyboard.tap_key('return')
    time.sleep(0.1)

'''
Terminate.
'''

file.close()
