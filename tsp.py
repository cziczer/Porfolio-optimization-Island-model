class TSP:
    def __init__(self, weight_matrix):
        self.weight_matrix = weight_matrix
        self.city_count = weight_matrix.shape[0]
        self.city_set = set(i for i in range(self.city_count))

    def _calculate_tour_distance(self, x):
        tour_dist = 0
        for i in range(1, len(x)):
            tour_dist += self.weight_matrix[int(x[i - 1]), int(x[i])]
        return tour_dist

    def fitness(self, path):
        # If there are duplicate genes in the chromosome, set its fitness to infintity.
        # Such chromosomes will not be fit for selection.
        x = [int(node) for node in path]
        if not (self.city_set == set(x)):
            res = float("inf")
        else:
            res = self._calculate_tour_distance(x)
        return [res]

    def get_bounds(self):
        """ Each chromosome has size : citycount and each gene is an integer between 0 and citycount-1"""
        return [0] * self.city_count, [self.city_count - 1] * self.city_count

    def get_nix(self):
        return self.city_count