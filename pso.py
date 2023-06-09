import numpy as np
import pygmo
import time

class PSO():
    def __init__(self, problem, eta1, eta2, variant, neighb_type, neighb_param, population_size=None):
        """
        :param problem: class defining problem we want to solve
        :param generations: number of generations
        :param eta1: social component
        :param eta2: cognitive component
        :param variant: algorithmic variant
            1 - Canonical (with inertia weight)
            2 - Same social and cognitive rand.
            3 - Same rand. for all components
            4 - Only one rand.
            5 - Canonical (with constriction fact.)
            6 - Fully Informed (FIPS)
        :param neighb_type: swarm topology (defining each particle’s neighbours)
            1 - gbest
            2 - lbest
            3 - Von Neumann
            4 - Adaptive random
        :param neighb_param: topology parameter (defines how many neighbours to consider)
        :param population_size: population size
        """
        self.problem = pygmo.problem(problem)
        self.population_count = population_size if population_size and population_size > self.problem.get_nx() else self.problem.get_nx()
        self.population = None # .get_x 2d array of population .champions_x - best solution
        self.algorithm = pygmo.algorithm(pygmo.pso(
            gen=self.problem.get_nx(),
            eta1=eta1,
            eta2=eta2,
            variant=variant,
            neighb_type=neighb_type,
            neighb_param=int(neighb_param * self.problem.get_nx())
        ))
        self.total_time = 0

    def run(self):
        start = time.time()
        if not self.population:
            self.population = pygmo.population(self.problem)
            for i in range(self.population_count):
                individual = list(np.random.permutation(self.population_count))
                self.population.push_back(x=individual)
        self.population = self.algorithm.evolve(self.population)
        self.total_time += (time.time() - start)

    def get_n_best_individuals(self, n):
        sorted_population_fitness_indexes = np.argsort(self.population.get_f().flatten())
        population_matrix = self.population.get_x()
        return [[int(node) for node in population_matrix[np.where(sorted_population_fitness_indexes == i)[0][0]]] for i
                in range(3)]

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
