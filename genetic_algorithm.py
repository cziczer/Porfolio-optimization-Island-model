import numpy as np
import pygmo
import time


class GeneticAlgorithm:
    def __init__(self, problem, cr, param_s, crossover, selection, population_size=None):
        """
        :param problem: class defining problem we want to solve
        :param generations: number of generations -> size of problem (1 iter of aco = size of problem iter of ga)
        :param population_size: size of population
        :param cr: crossover probability
        :param eta_c: distribution index for sbx crossover. This parameter is inactive if other types of crossover are selected
        :param m: mutation probability
        :param param_m: distribution index (polynomial mutation), gaussian width (gaussian mutation) or inactive (uniform mutation)
        :param param_s: the number of best individuals to use in “truncated” selection or the size of the tournament in tournament selection
        :param crossover: the crossover strategy. One of exponential, binomial, single or sbx
        :param mutation: the mutation strategy. One of gaussian, polynomial or uniform
        :param selection: the selection strategy. One of tournament, “truncated”
        """
        self.problem = pygmo.problem(problem)
        self.population_count = population_size if population_size and population_size > self.problem.get_nx() else self.problem.get_nx()
        self.population = None # .get_x 2d array of population .champions_x - best solution
        self.algorithm = pygmo.algorithm(pygmo.sga(
            gen=self.problem.get_nx(),
            cr=cr,
            eta_c=1.0,
            m=0,
            param_m=0,
            param_s=int(param_s * self.problem.get_nx()),
            crossover=crossover,
            mutation="uniform", # we don't want to have mutations here so this doesn't matter
            selection=selection
        ))
        self.total_time = 0

    def run(self):
        start = time.time()
        if not self.population:
            self.population = pygmo.population(self.problem)
            for i in range(self.population_count):
                individual = list(map(float, np.random.permutation(self.population_count)))
                self.population.push_back(x=individual)
        self.population = self.algorithm.evolve(self.population)
        self.total_time += (time.time() - start)

    def get_n_best_individuals(self, n):
        sorted_population_fitness_indexes = np.argsort(self.population.get_f().flatten())
        population_matrix = self.population.get_x()
        return [[int(node) for node in population_matrix[np.where(sorted_population_fitness_indexes == i)[0][0]]] for i
                in range(n)]

    def get_best_individual_with_cost(self):
        return self.population.champion_x, self.population.champion_f[0]

    def receive_migration(self, new_population_part, n):
        new_population = pygmo.population(self.problem)
        sorted_population_fitness_indexes = np.argsort(self.population.get_f().flatten())
        population_matrix = self.population.get_x()
        for i in range(sorted_population_fitness_indexes.shape[0] - n):
            new_population.push_back(x=[int(node) for node in population_matrix[np.where(sorted_population_fitness_indexes == i)[0][0]]])
        for migrated_individual in new_population_part:
            new_population.push_back(x=migrated_individual)
        self.population = new_population