import time
import networkx as nx
from genetic_algorithm import GeneticAlgorithm
from pso import PSO
from aco import ACO
from copy import deepcopy
import acopy


class IslandModel:
    def __init__(self, configs, migration_rates, iterations, aco_migration_evaporation_rate):
        self.iterations = iterations
        # configs -> list of touples 'algo name', dict with config
        # factory - name, config - unwrap with asterix
        # how many iteration for each algorithm per one island iteration
        # keep track of best score
        # stop codition ? -> value < threshold or # of iterations or run until we find solution?
        self.aco_migration_evaporation_rate = aco_migration_evaporation_rate
        self.migration_rates = migration_rates # int - how many individuals we migrate
        self.models = [self.model_factory(model_name, config) for model_name, config in configs]
        self.progress = []

    def model_factory(self, model_name, config):
        if model_name == 'aco':
            return ACO(**config)
        if model_name == 'pso':
            return PSO(**config)
        return GeneticAlgorithm(**config)

    def run(self):
        # measure time here
        # we measure time pseudo parallel - do we stop counting some parts like translations and so on or not?
        # propose - we measure iterations -> how many island iteration stands compare to how many iterations in given algorithm
        start = time.time()
        for i in range(self.iterations):
            self.run_iteration()
            best_path, cost = self.get_best_solution()
            # print(f'Best solution: {best_path} with cost {cost}')
            # print(f"Iteration - {i}, cost best patch - {cost}")
            self.progress.append(cost)
        stop = time.time()
        print(f'Total time: {stop - start} s')

    def get_best_solution(self):
        best_path = None
        lowest_cost = float('inf')
        for model in self.models:
            model_best_path, model_lowest_cost = model.get_best_individual_with_cost()
            if model_lowest_cost < lowest_cost:
                lowest_cost = model_lowest_cost
                best_path = model_best_path
        return best_path, lowest_cost

    def run_iteration(self):
        # ring topology, 1 -> 2, 2->3 , ..., -1 -> 0,...
        # but first we ran all of them then, then migrations
        for model in self.models:
            model.run()
        for i, model in enumerate(self.models):
            self.migration(model, self.models[(i+1)%len(self.models)], i)

    def migration(self, model_1, model_2, model_idx):
        # model_1 -> take from population
        # model_2 -> receives population
        # translate and exchange population here we decide what migration algo use
        is_model_1_aco = isinstance(model_1, ACO)
        is_model_2_aco = isinstance(model_2, ACO)
        new_population = None
        migration_rate = self.migration_rates[int(model_idx)]
        if is_model_1_aco and is_model_2_aco:
            new_population = self.translation_aco_to_ga_pso(model_1, model_idx)
            model_2.receive_migration(new_population, migration_rate, from_aco=True)

        if is_model_1_aco and not is_model_2_aco:
            new_population = self.translation_aco_to_ga_pso(model_1, model_idx)
            model_2.receive_migration(new_population, migration_rate)

        else:
            new_population = self.get_migration_population_from_pso_ga(model_1, model_idx)
            model_2.receive_migration(new_population, migration_rate)


    def translation_aco_to_ga_pso(self, aco_model, model_idx):
        # evaporation based translation
        pheromone_table_copy = deepcopy(aco_model.get_pheromone_table())
        new_population = []
        migration_rate = self.migration_rates[int(model_idx)]
        for i in range(migration_rate):
            tour = acopy.ant.Ant().tour(deepcopy(pheromone_table_copy)).nodes
            new_population.append(tour)
            for k in range(1, len(tour)):
                j = k-1
                pheromone_table_copy._adj[tour[j]][tour[k]]['pheromone'] = (1-self.aco_migration_evaporation_rate) * pheromone_table_copy._adj[tour[j]][tour[k]]['pheromone']

        return new_population

    def get_migration_population_from_pso_ga(self, model, model_idx):
        migration_rate = self.migration_rates[int(model_idx)]
        return model.get_n_best_individuals(n=migration_rate)
