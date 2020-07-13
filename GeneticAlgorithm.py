import numpy as np
from Car import Car


class GeneticAlgorithm(object):
    def __init__(self, population_size, mutation_rate):
        self.pop_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = 0

    def create_population(self, input_size):
        self.pop = []
        self.nodes = input_size
        for _ in range(self.pop_size):
            car = Car()
            car.get_genes(self.nodes, genes=[[[1.3001829422392683, 0.8000856027691232, -1.5785073281530515, -2.8647414187322386, -0.7141955007518759, -0.3670487821346391, -3.7998092630225644, -4.405835967094093, 2.0557444816390857, -0.09336194023387456, -0.7266628432639095, 0.5002341909216479, 0.32317776785895425, -1.9559411100920112, 0.14616350746591955], [-0.6300914796369126, -2.25749173353568, 1.4792635329477752, -0.3327470291154955, 4.9655237160018455, -1.3673537444481587, -1.603815188875779, -3.187818364141801, 3.12763867621749], [-1.125398828359506, -3.460349939960378, 3.0711242443193996]], [[4.226548855181022, 4.291171140731139, -2.424117565430474], [-4.9718817032241525, -0.6808755943276221, -4.768670702354022], [0.9272046954287498]]])
            # print("Car Genes_____", car.genes)
            self.pop.append(car)

    def calc_score(self):
        # This calculates the score of each car based on the number of checkpoints reached
        self.score = []
        for car in self.pop:
            self.score.append(car.score)

    def acceptReject(self):
        # Returns a car from self.pop based on the weighted score
        check = 0
        while True:
            index = np.random.randint(0,len(self.pop))
            r = np.random.rand() * self.maxScore
            if r < self.score[index]:
                return self.pop[index]
            check+=1
            if check == 10000:
                return None

    def crossover(self, partner1, partner2):
        # The issue is here, I need to update the genes
        # Am I changing partner1 instead of
        new_genes = rand_genes(self.nodes, 0)
        for lists in range(len(partner1.genes)):
            for list in range(len(partner1.genes[lists])):
                for item in range(len(partner1.genes[lists][list])):
                    if np.random.rand() < .5:
                        new_genes[lists][list][item] = partner1.genes[lists][list][item]
                    else:
                        new_genes[lists][list][item] = partner2.genes[lists][list][item]
        child = Car()
        child.get_genes(self.nodes, genes=new_genes)
        return child

    def mutate(self, car):
        for lists in range(len(car.genes)):
            for list in range(len(car.genes[lists])):
                for item in range(len(car.genes[lists][list])):
                    if self.mutation_rate > np.random.random():
                        val = np.random.rand()*2-1
                        car.genes[lists][list][item] = val
                        if car.genes[lists][list][item] > 10:
                            car.genes[lists][list][item] = 10
                        elif car.genes[lists][list][item] < -10:
                            car.genes[lists][list][item] = -10
        return car

    def evolve(self):
        # First find the maximum score of the cars
        maxIndex = 0
        maxVal = 0
        for i in range(len(self.pop)):
            if self.score[i] > maxVal:
                maxVal = self.score[i]
                maxIndex = i
        self.maxScore = self.score[maxIndex]
        self.bestGenes = self.pop[maxIndex].genes
        # Then select two parents and create a child from their genes
        # This happens until a complete new generation is created
        newPop = []
        for i in range(len(self.pop)):
            partner1 = self.acceptReject()
            partner2 = self.acceptReject()
            child = self.crossover(partner1, partner2)
            child = self.mutate(child)
            newPop.append(child)
            self.pop[i].delete()
        self.pop = newPop
        self.generations += 1

def rand_genes(nodes, val):
    genes = []
    weights = []
    biases = []
    # Weights
    for layer in range(len(nodes)-1):
        w = []
        for node1 in range(nodes[layer]):
            for node2 in range(nodes[layer+1]):
                w.append(val)
        weights.append(w)
    genes.append(weights)
    # Biases
    for i in nodes[1:]: # Should this only go until -1?
        b = []
        for node in range(i):
            b.append(val)
        biases.append(b)
    genes.append(biases)
    return genes
