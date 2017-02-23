import numpy as np
import sys
import math
import pickle
from collections import namedtuple
import preprocess as data


class Cromosome(object):
    def __init__(self, initialize=True):
        self.values = []
        self.score = None

        if (not initialize): return

        for i in range(data.num_cache_server):
            self.values.append(self.init_cashe())

    def evaluate(self):
        self.score = 0
        total_requests = 0
        for request in data.requests:
            total_requests += request.n
            l = data.latency_d[request.e]
            for server_index, server in enumerate(self.values):
                latency = data.endpoints[request.e].get(server_index, None)
                if latency and latency < l and request.v in server:
                    l = latency
            self.score += request.n * (data.latency_d[request.e]-l)
        self.score /= total_requests


    def init_cashe(self):
        cashe_size = 0
        cashe = set()
        videos = np.random.permutation(data.num_videos)
        for video in videos:
            if cashe_size + data.video_sizes[video] <= data.capacity_each_cache:
                cashe.add(video)
                cashe_size += data.video_sizes[video]
        return cashe
             
    def save(self, name):
        with open(name, 'wb') as handle:
            pickle.dump(self.values, handle)
        with open(name + ".txt", 'w') as f:
            f.write(str(data.num_cache_server) + "\n")
            for i, server in enumerate(self.values):
                f.write(str(i))
                for video in server:
                    f.write(" " + str(video))
                f.write("\n")



class GeneticAlgorithm(object):

    def __init__(self, example_name, p_m=0.01):
        self._p_m = p_m
        self.best = None
        self.example_name = example_name

    def evaluate(self, population):
        for cromosome in population:
            cromosome.evaluate()

    def getBest(self, population):
        population.sort(key = lambda x: x.score)
        return population[-1]

    def cross(self, parent1, parent2):
        child = Cromosome(False)
        r = np.random.randint(0, 2, data.num_cache_server)
        for i, r_i in enumerate(r):
            child += [parent1[i]] if r_i == 0 else [parent2[i]]
        return child
    
    def mutate(self, cromosome):
        for i in range(len(cromosome.values)):
            if np.random.uniform(0, 1) <= self._p_m:
                cromosome.values[i] = self.init_cashe()
    
    def createPopulation(self, size):
        population = []
        for i in range(size):
            population.append(Cromosome())
        return population
    
    def run(self, size, iterations):
        population = self.createPopulation(size)
        self.evaluate(population)
        self.best = self.getBest(population)
        last_best = self.best
        print ("Best: ", self.best.score)
        self.best.save(self.example_name)
        for i in range(iterations):
            best = self.getBest(population)
            if (best.score > last_best.score):
                self.best = best
                last_best = best
                print (best.values, " Generacija: ", i, "Score: ", best.score)
                self.best.save(self.example_name)
            population = self.selection(population)
        return self.getBest(population)

class EliminationGeneticAlgorithm(GeneticAlgorithm):

    def __init__(self, example_name, p_m=0.01):
        super(EliminationGeneticAlgorithm, self).__init__(example_name, p_m)

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
        parents_indexes.sort(key = lambda x: population[x].score)
        child = self.cross(population[parents_indexes[-1]], population[parents_indexes[-2]])
        #print population[parents_indexes[0]].error, population[parents_indexes[1]].error, population[parents_indexes[2]].error
        self.mutate(child)
        self.evaluate([child], self._data)
        population[parents_indexes[0]] = child
        if (child.score > self.best.score): self.best = child
        return population

if __name__=="__main__":
    algorithm = EliminationGeneticAlgorithm(data.example_name)
    algorithm.run(10, 100000000)



