import tsplib95
import networkx as nx #-> AS G = nx.Graph() -> nx.from_numpy_matrix(aa)
from tsp import TSP
from copy import deepcopy
from configs import tsp_configs
from island_model import IslandModel
import sys
import json
import traceback
import os

configs_list = [
    # "aco_1__3",
    "aco_1__4_2", 
    "ga_9_35_exponential_tournament", 
    # "ga_8_6_single_tournament",
    # "pso_2_05__2_05__1__2__25",
    # "pso_2_05__1_3__6__1__4"
]

def get_migrations(migration_id, islands_count, migration_slice=0):
    all_posiible = [0.07,  0.125, 0.15]#, 0.2, .6, .75]
    result = []
    if islands_count < 2: 
        return [0]
    elif islands_count == 2:
        for i, el in enumerate(all_posiible):
            for j in range(i, len(all_posiible)):
                result.append((el, all_posiible[j]))
        return result[migration_id*migration_slice: (migration_id+1)*migration_slice]
    return all_posiible

def run_experiments(iterations, migration_id, islands_count, G, tsp_instance, problem_size, exp_id, migration_slice=1):
    for a, b in get_migrations(migration_id, islands_count, migration_slice):
        for migration_a, migration_b in [(a, b), (b, a)]:
            for i in [0]:
                for j in [1]:
                    # set up pair of metaheuristics
                    model_1_name = configs_list[i]
                    model_2_name = configs_list[j]
                    model_1 = tsp_configs[model_1_name]
                    model_2 = tsp_configs[model_2_name]

                    # add problem to algo config
                    if model_1_name[:3] == 'aco':
                        model_1[1]['graph'] = deepcopy(G)
                    else:
                        model_1[1]['problem'] = tsp_instance

                    if model_2_name[:3] == 'aco':
                        model_2[1]['graph'] = deepcopy(G)
                    else:
                        model_2[1]['problem'] = tsp_instance

                    migration_rates = [int(migration_a * problem_size), int(migration_b * problem_size)]
                    island_model = IslandModel(
                        configs=[model_1, model_2],
                        migration_rates=migration_rates,
                        iterations=iterations,
                        aco_migration_evaporation_rate=.01
                    )

                    try:
                        island_model.run()
                        if f"{exp_id}_{tsp_name}.json" not in os.listdir():
                            with open(f"{exp_id}_{tsp_name}.json", "w+") as f:
                                pass
                        f = open(f"{exp_id}_{tsp_name}.json", 'r+')
                        # First we load existing data into a dict.
                        try:
                            saved_results = json.load(f)
                        except json.JSONDecodeError as e:
                            saved_results = {}
                        # Join new_data with file_data inside emp_details
                        saved_results[f'{model_1_name}_{model_2_name}_migration_{int(migration_a*100)}_{int(migration_b*100)}'] = island_model.progress
                        # Sets file's curren t position at offset.
                        f.close()
                        with open(f"{exp_id}_{tsp_name}.json", 'w+') as f:
                            # f.seek(0)
                            # convert back to json.
                            json.dump(saved_results, f, indent=4)
                    except Exception as e:
                        print(e)
                        print(traceback.print_exc())
                        print()
    

def run_experiment(tsp_name, iterations, exp_id, migration_id, islands_count, migration_slice):    
    problem = tsplib95.load(f'tsp_data/{tsp_name}.tsp')
    G = problem.get_graph()
    matrix = nx.to_numpy_matrix(G)
    problem_size = matrix.shape[0]
    tsp_instance = TSP(matrix)

    run_experiments(iterations, migration_id, islands_count, G, tsp_instance, problem_size, exp_id, migration_slice)


if __name__ == '__main__':
    tsp_name = "bier127"
    iterations = 2
    e_id = 1
    migration_id = 0
    islands_count = 2
    migration_slice = 1
    run_experiment(tsp_name, iterations, e_id, migration_id, islands_count, migration_slice)
