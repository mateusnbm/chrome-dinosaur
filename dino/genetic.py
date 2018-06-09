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

        self.fitnesses = [0]
        self.genes = [random.uniform(0, 1) for _ in range(length)]

    '''
    '''

    def __str__(self):

        str_rep = ""

        for gene in self.genes:

            str_rep += str(gene) + ", "

        str_rep += str(self.fitnesses[-1])

        return str_rep

    '''
    '''

    def add_fitness(self, fitness):

        self.fitnesses.append(fitness)

        if len(self.fitnesses) > 5:

            self.fitnesses = self.fitnesses[-5:]

    '''
    '''

    def get_fitness(self):

        return sum(self.fitnesses)/len(self.fitnesses)      

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

            parent_a.fitnesses = [0]
            parent_a.genes = pa_part_a + pb_part_b

            parent_b.fitnesses = [0]
            parent_b.genes = pb_part_a + pa_part_b

        return parent_a, parent_b


    '''
    '''

    def mutate(self, probability):

        rdn = random.randint(1, 100)
        prb = probability * 100

        if rdn > prb:

            for i in range(len(self.genes)):

                self.genes[i] *= random.uniform(0, 1)
