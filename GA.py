import numpy as np
import sys
import math
from collections import namedtuple


class Cromosome(object):
    def __init__(self):
        self.values = np.random.uniform(-4, 4, 5)
        self.error = None

    def getOutput(self, x, y):
        b0, b1, b2, b3, b4 = self.values
        return np.sin(b0 + b1*x) + b2*np.cos(x*(b3+y)) / (1 + np.e**((x-b4)**2))

class GeneticAlgorithm(object):

    def __init__(self, data, p_m=0.01):
        self._data = data
        self._p_m = p_m
        self.best = None

    def evaluate(self, population, data):
        for cromosome in population:
            cromosome.error = np.sum((cromosome.getOutput(data.x, data.y) - data.output)**2) / len(data.x)

    def getBest(self, population):
        population.sort(key = lambda x: x.error)
        return population[0]

    def cross(self, parent1, parent2):
        child = Cromosome()
        for i in range(len(parent1.values)):
            if (parent1.values[i] < parent2.values[i]):
                child.values[i] = np.random.uniform(parent1.values[i], parent2.values[i]);
            else:
                child.values[i] = np.random.uniform(parent2.values[i], parent1.values[i]);
        return child
    
    def mutate(self, cromosome):
        for i in range(len(cromosome.values)):
            if np.random.uniform(0, 1) <= self._p_m:
                cromosome.values[i] = np.random.uniform(-4, 4)
    
    def createPopulation(self, size):
        population = []
        for i in range(size):
            population.append(Cromosome())
        return population
    
    def run(self, size, error_treshold, iterations):
        population = self.createPopulation(size)
        self.evaluate(population, self._data)
        self.best = self.getBest(population)
        last_best = self.best
        for i in range(iterations):
            best = self.getBest(population)
            if (best.error < last_best.error):
                self.best = best
                last_best = best
                print best.values, " Generacija: ", i, "Error: ", best.error
            if best.error <= error_treshold: return best
            population = self.selection(population)
        return self.getBest(population)

class EliminationGeneticAlgorithm(GeneticAlgorithm):

    def __init__(self, data, p_m=0.01):
        super(EliminationGeneticAlgorithm, self).__init__(data, p_m)

    def chooseParents(self, population):
        i1, i2, i3 = np.random.randint(0, len(population), 3)
        while i1 == i2 or i1 == i3 or i2 == i3:
            i1, i2, i3 = np.random.randint(0, len(population), 3)
        return [i1, i2, i3]

    def getBest(self, population):
        if self.best: return self.best
        return super(EliminationGeneticAlgorithm, self).getBest(population)

    def selection(self, population):
        parents_indexes = self.chooseParents(population)
        parents_indexes.sort(key = lambda x: population[x].error)
        child = self.cross(population[parents_indexes[0]], population[parents_indexes[1]])
        #print population[parents_indexes[0]].error, population[parents_indexes[1]].error, population[parents_indexes[2]].error
        self.mutate(child)
        self.evaluate([child], self._data)
        population[parents_indexes[2]] = child
        if (child.error < self.best.error): self.best = child
        return population



