import numpy as np
from Car import Car

class NeuralNet(object):
    """
    layers
    nodes per layer
    initialize random values for the weights and biases

    Using a feed forward system with 3 to 5 inputs and possibly 3-4 layers.
    The inputs will be distances recorded at different angles of the car.
    These angles will let the car know how close it is to obstacles
    Genetic algorithm used to train the car

    Need a method for saving the "mind" of the top car at the end.  Have a
    way of starting with a specific brain.
    """

    def __init__(self, genes, inputs):
        self.layers = len(genes[0])
        self.weights = genes[0]
        self.biases = genes[1]
        self.h = self.feed_forward(inputs)

    def sigmoid(self, x):
        return 1.0 / (1.0 + np.exp(-x))

    def feed_forward(self, inputs):
        in_ = inputs
        for layer in range(self.layers):
            count = 0
            a = 0
            h = []
            for nodes in range(len(self.biases[layer])):
                CONST = int(len(self.weights[layer]) / len(self.biases[layer]))
                for i in range(CONST):
                    a += self.weights[layer][nodes * CONST + i] * in_[i]
                    # print(nodes * int(len(self.weights[layer]) / len(self.biases[layer])) + i, "now")
                    count += 1
                    # a =
                h.append(self.sigmoid(a+self.biases[layer][nodes]))
            # print(count,h)
            in_ = h
        return h[0] * 2 - 1


class GeneticAlgorithm(object):
    def __init__(self, population_size, mutation_rate):
        self.pop_size = population_size
        self.mutation_rate = mutation_rate

    def create_population(self, population_size, input_size):
        self.pop = []
        for _ in range(population_size):
            dna = DNA(input_size)
            car = Car(x=500,y=85)
            car.get_genes(dna.genes)
            self.pop.append([dna,car])

    def calc_fitness(self):
        for car in range(len(self.pop)):
            self.pop[car][0].fitness = self.pop[car][1].score

    def evolve(self):
        self.maxFitness = 0
        for i in range(len(self.pop)):
            if self.pop[i][0].fitness > self.maxFitness:
                self.maxFitness = self.pop[i][0].fitness
        newPop = []
        for i in range(len(self.pop)):
            partnerA = self.acceptReject()
            partnerB = self.acceptReject()
            child = partnerA.crossover(partnerB)
            child.mutate(self.mutationRate)
            kid_car = Car(x=500,y=85)
            kid_car.get_genes(child.nodes, child)
            newPop.append([child,kid_car])
        self.pop = newPop
        self.generations += 1

    def acceptReject(self):
        check = 0
        while True:
            index = np.random.randint(0,len(self.pop))
            partner = self.pop[index][0]
            r = np.random.rand() * self.maxFitness
            if r < partner.fitness:
                return partner
            check+=1
            if check == 10000:
                return None


class DNA(object):
    def __init__(self,input_size,genes=None):
        self.nodes = input_size
        self.fitness = 0
        if not genes:
            self.rand_genes()

    def rand_genes(self):
        self.genes = []
        self.weights = []
        self.biases = []
        # Weights
        for layer in range(len(self.nodes)-1):
            w = []
            for node1 in range(self.nodes[layer]):
                for node2 in range(self.nodes[layer+1]):
                    w.append(np.random.random()*2-1)
            self.weights.append(w)
        self.genes.append(self.weights)
        # Biases
        for i in self.nodes[1:]: # Should this only go until -1?
            b = []
            for node in range(i):
                b.append(np.random.random()*2-1)
            self.biases.append(b)
        self.genes.append(self.biases)
        print("DNA Genes Created", self.genes)

    # def fitnessDNA(self,target):
    #     score = 0
    #     for point in self.checkpoints:
    #         score += 1
    #     self.fitness = score**2 / target**2

    def crossover(self, partner):
        child = DNA(len(self.nodes))
        midpoint = np.random.randint(0,len(self.genes))
        for lists in range(len(self.genes)):
            for list in lists:
                for item in list:
                    if np.random.rand() > midpoint:
                        child.genes[lists][list][item] = self.genes[lists][list][item]
                    else:
                        child.genes[lists][list][item] = partner.genes[lists][list][item]
        return child

    def mutate(self, mutation_rate):
        for lists in range(len(self.genes)):
            for list in lists:
                for item in list:
                    if mutation_rate > np.random.random():
                        self.genes[lists][list][item] = np.random.rand()*2-1


# neuron_shape = (5,4,3,1)
# input_parameters = [.1,.1,.1,.1,.1]
# h = []
# for i in range(1):
#     Howdy = DNA(neuron_shape)
#     Net = NeuralNet(Howdy.genes, input_parameters)
#     h.append(Net.h)
# print(min(h),max(h))
# """
# make the genetic algorith.  mutation rate .01, pop size 20
# This creates our initial set of random DNA
# Use this DNA to create a car
# This car will then
# """
