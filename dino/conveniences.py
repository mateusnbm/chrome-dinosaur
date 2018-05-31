#
# conveniences.py
#


import csv

from dino.genetic import Genome


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
        genome.fitness = reader[-i-1][-1]

        genomes.append(genome)

    return genomes
