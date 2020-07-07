# Hereditary - process at which children recieve properties of their parents
# Variation - Variety of traits or a means to produce variation
# Selection - Some children must be able to pass on genetic information to children

# 1. Create a pop of n elements with random genetics
# 2a. Calculate fitness for n elements
# 2b. Reproduction and selection
# Select parents. Every item has a chance to be picked, ranked probability by fitness score
# Crossover combines the parents to make a child
# Mutation changes the child slightly to get variation

import numpy as np

class Population(object):
    def __init__(self,target,populationSize,mutationRate):
        # self.populationSize = populationSize
        self.mutationRate = mutationRate
        self.target = target
        self.finished = False
        self.perfectScore = 1
        self.generations = 0
        self.best = ''

        self.population = []
        for i in range(populationSize):
            self.population.append(DNA(len(self.target)))
        self.calcFitness()

    def calcFitness(self):
        for i in range(len(self.population)):
            self.population[i].fitnessDNA(self.target)
    def generate(self):
        self.maxFitness = 0
        for i in range(len(self.population)):
            if self.population[i].fitness > self.maxFitness:
                self.maxFitness = self.population[i].fitness
        newPop = []
        for i in range(len(self.population)):
            partnerA = self.acceptReject()
            partnerB = self.acceptReject()
            child = partnerA.crossover(partnerB)
            child.mutate(self.mutationRate)
            newPop.append(child)
        self.population = newPop
        self.generations += 1

    def acceptReject(self):
        check = 0
        while True:
            index = np.random.randint(0,len(self.population))
            partner = self.population[index]
            r = np.random.rand() * self.maxFitness
            if r < partner.fitness:
                return partner
            check +=1
            if check == 10000:
                return None

    def getBest(self):
        self.best = 0
        index = 0
        output = ''
        for i in range(len(self.population)):
            if self.population[i].fitness > self.best:
                index = i
                self.best = self.population[i].fitness
        for char in self.population[index].genes:
            output += char
        print(output, self.population[index].fitness)
        return output


class DNA(object):
    def __init__(self,length):
        self.genes = []
        self.newPhrase = ''
        self.fitness = 0
        for i in range(length):
            c = newChar()
            self.genes.append(c)
            self.newPhrase += str(c)
        # print('newPhrase' + str(self.newPhrase))
    def fitnessDNA(self,target):
        score = 0
        for i in range(len(self.genes)):
            if self.genes[i] == target[i]:
                score += 1
        self.fitness = score**4 / len(target)**4
        # self.fitness = self.fitness**4
    def crossover(self,partner):
        child = DNA(len(self.genes))
        midpoint = np.random.randint(0,len(self.genes))
        for i in range(len(self.genes)):
            if i > midpoint:
                child.genes[i] = self.genes[i]
            else:
                child.genes[i] = partner.genes[i]
        return child
    def mutate(self,mutationRate):
        for i in range(len(self.genes)):
            if mutationRate > np.random.random():
                self.genes[i] = chr(np.random.randint(32,128))

def newChar():
    c = np.random.randint(63,123)
    if c == 63: c = 32
    if c == 64: c = 33
    return chr(c)

def run():
    goal = 'Genetic Algorithm'
    popSize = 100
    mutationRate = 0.04
    population = Population(goal,popSize,mutationRate)
    while True:
        population.generate()
        population.calcFitness()
        hi = population.getBest()

        if goal == hi:
            print('This took ' + str(population.generations) + ' generations!')
            break

if __name__ == '__main__':
    run()
