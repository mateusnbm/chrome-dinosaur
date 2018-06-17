#
# conveniences.py
#


import csv
import time

from pykeyboard import PyKeyboard

from dino.genetic import Genome


'''
'''

def set_output(output, last_output, last_output_timestamp):

    keyboard = PyKeyboard()

    if output > 0.55:

        keyboard.release_key('down')
        keyboard.tap_key('space')
        time.sleep(0.5)

    elif output < 0.45:

        keyboard.press_key('down')

    else:

        keyboard.release_key('down')

    return 0, 0


'''
'''

def load_genomes_from_file(filename, genomes_count, genomes_size):

    genomes = []

    file = open(filename, 'r')
    reader = list(csv.reader(file))
    file.close()

    for i in range(genomes_count):

        genome = Genome(length=genomes_size)
        genome.genes = reader[-i-1][:-1]
        genome.fitness = float(reader[-i-1][-1])
        genome.genes = [float(x) for x in genome.genes]

        genomes.append(genome)

    return genomes
