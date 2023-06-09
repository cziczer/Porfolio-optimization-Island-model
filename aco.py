import acopy
import time

class ACO:
    def __init__(self, graph, alpha=1, beta=3, rho=.03, q=1, population_size=None):
        """
        :param graph: tsp problem as a nx graph
        :param alpha: (float) – relative factor for edge pheromone
        :param beta: (float) – relative factor for edge weight
        :param rho: (float) – percentage of pheromone that evaporates each iteration
        :param q: (float) – amount of pheromone each ant can deposit
        :param max_iter: (int) - max iterations per run
        :param gen_size: (int) – number of Ant s to use (default is one per graph node)
        """
        self.colony = acopy.Colony(alpha=alpha, beta=beta)
        self.solver = acopy.Solver(rho=rho, q=q)
        self.q = q
        self.rho = rho
        self.max_iter = 1
        self.gen_size = population_size if population_size and population_size > graph.number_of_nodes() else graph.number_of_nodes()
        self.graph = graph
        self._pheromone_table = None
        self.last_tour = None
        self.total_time = 0

    def run(self):
        """
        tour - tour.nodes / tour.path to get the best solution found in this run
        """
        start = time.time()
        if self._pheromone_table:
            tour = self.solver.solve(self._pheromone_table, self.colony, limit=self.max_iter, gen_size=self.gen_size)
        else:
            tour = self.solver.solve(self.graph, self.colony, limit=self.max_iter, gen_size=self.gen_size)
        self.set_pheromone_table(tour.graph)
        self.last_tour = tour
        self.total_time += (time.time() - start)

    def get_pheromone_table(self):
        """
        :return: pheromone table as dict:
            ...
            '_adj':
                {
                    node: {
                        connected_node: {weight: x, pheromone: y}
                        ...
                }
        """
        return self._pheromone_table

    def set_pheromone_table(self, pheromone_table):
        self._pheromone_table = pheromone_table

    def get_best_individual_with_cost(self):
        return self.last_tour.nodes, self.last_tour.cost

    def receive_migration(self, new_population_part, n, from_aco=False):
        for individual in new_population_part:
            for j in range(1, len(individual)):
                # in ga and pso we have numpy  matrix, and nodes starts from 0, in pheromon table we have graph and we count from 1
                if from_aco:
                    node_j = individual[j]
                    node_i = individual[j - 1]
                else:
                    if 0 in self._pheromone_table._adj: # dodajemy albo nie w zaleznosci jak sa trzymane dane XD
                        node_j = individual[j]
                        node_i = individual[j-1]
                    else:
                        node_j = individual[j] + 1
                        node_i = individual[j - 1] + 1
                try:
                    self._pheromone_table._adj[node_i][node_j]['pheromone'] += self.q * (1 / self._pheromone_table._adj[node_i][node_j]['weight'])
                except Exception as e:
                    print(e)
                    print(node_i, node_j)