#
# genetic.py
#


import copy
import random


'''
'''

class Genome():

    '''
    '''

    def __init__(self, length):

        self.fitness = -1
        self.genes = [random.uniform(0, 1) for _ in range(length)]

    '''
    '''

    def __str__(self):

        str_rep = ""

        for gene in self.genes:

            str_rep += str(gene) + ", "

        str_rep += str(self.fitness)

        return str_rep

    '''
    '''

    def recombine(self, mate, probability):

        rdn = random.randint(1, 100)
        prb = probability * 100

        parent_a = copy.deepcopy(self)
        parent_b = copy.deepcopy(mate)

        if rdn > prb:

            cut_index = random.randint(0, len(self.genes)-1)

            pa_part_a = parent_a.genes[:cut_index]
            pa_part_b = parent_a.genes[cut_index:]
            pb_part_a = parent_b.genes[:cut_index]
            pb_part_b = parent_b.genes[cut_index:]

            parent_a.fitness = -1
            parent_a.genes = pa_part_a + pb_part_b

            parent_b.fitness = -1
            parent_b.genes = pb_part_a + pa_part_b

        return parent_a, parent_b


    '''
    '''

    def mutate(self, probability):

        rdn = random.randint(1, 100)
        prb = probability * 100

        if rdn > prb:

            mutation_index = random.randint(0, len(self.genes)-1)

            self.genes[mutation_index] *= random.uniform(0, 1)
