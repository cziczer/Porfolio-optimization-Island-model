import json
import matplotlib.pyplot as plt
import os


def process_and_save_single_results(tsp_name):
    f1_json = json.load(open(f"1_{tsp_name}_single.json", 'r'))
    f2_json = json.load(open(f"2_{tsp_name}_single.json", 'r'))
    f3_json = json.load(open(f"3_{tsp_name}_single.json", 'r'))
    for key in f3_json.keys():
        res_1 = f1_json[key]
        res_2 = f2_json[key]
        res_3 = f2_json[key]
        res = []
        for i in range(len(res_3)):
            mean = (res_3[i] + res_2[i] + res_1[i]) / 3
            res.append(int(mean))
        if f"results_single_{tsp_name}.json" not in os.listdir():
            with open(f"results_single_{tsp_name}.json", "w+") as f:
                json.dump({}, f, indent=4)
        with open(f"results_single_{tsp_name}.json", 'r+') as f:
            saved_results = json.load(f)
            saved_results[key] = res
            f.seek(0)
            json.dump(saved_results, f, indent=4)


def process_and_save_island_model_results(tsp_name, is_3_island, files_count=1):
    result_file_name = f"results_3islands_{tsp_name}.json" if is_3_island else f"results_{tsp_name}.json"
    for i in range(files_count):
        data = {}
        if is_3_island:
            f1_json =  json.load(open(f"1_{tsp_name}.json", 'r'))
            f2_json =  json.load(open(f"2_{tsp_name}.json", 'r'))
        else:
            f1_json =  json.load(open(f"1_{i}_{tsp_name}.json", 'r'))
            f2_json =  json.load(open(f"2_{i}_{tsp_name}.json", 'r'))
        for key in f2_json.keys():
            res_1 = f1_json.get(key)
            res_2 = f2_json.get(key)
            res = []
            if res_1:
                for i in range(len(res_2)):
                    try:
                        mean = (res_2[i] + res_1[i]) / 2
                    except:
                        mean = res_2[i]
                    res.append(int(mean))
            else:
                res = res_2
            if result_file_name not in os.listdir():
                with open(result_file_name, "w+") as f:
                    json.dump({}, f, indent=4)
            with open(result_file_name, 'r+') as f:
                saved_results = json.load(f)
                saved_results[key] = res
                f.seek(0)
                json.dump(saved_results, f, indent=4)
        for key in f1_json.keys():
            res_1 = f1_json.get(key)
            res_2 = f2_json.get(key)
            res = []
            if res_2:
                for i in range(len(res_2)):
                    mean = (res_2[i] + res_1[i]) / 2
                    res.append(int(mean))
            else:
                res = res_1
            with open(result_file_name, 'r+') as f:
                saved_results = json.load(f)
                saved_results[key] = res
                f.seek(0)
                json.dump(saved_results, f, indent=4)


def load_result_file(model_type, tsp_name):
    results = open(f"results{model_type}_{tsp_name}.json", 'r')
    return json.load(results)


def sort_results(results):
    return [(k, v) for k, v in sorted(results.items(), key=lambda item: min(item[1]))]


def plot_one_type_results(title, raw_data):
    fig, ax = plt.subplots(figsize=(16, 16))
    for key, data in raw_data:
        for i in range(1, len(data)):
            data[i] = min(data[i], data[i-1])
        ax.plot([i* int(60 / len(data)) *127 for i in range(len(data))], data)
    ax.grid()
    plt.xlabel('Iterations', size=12)
    plt.ylabel('Cost', size=12)
    plt.title(title, size=32)
    plt.show()


def plot_and_compare(title, raw_data_1, raw_data_2):
    fig, ax = plt.subplots(figsize=(16, 16))
    for key, data in raw_data_1:
        for i in range(1, len(data)):
            data[i] = min(data[i], data[i-1])
        ax.plot([i*int(60/len(data))*127 for i in range(len(data))], data, linestyle='dashed')
    for key, data in raw_data_2:
        for i in range(1, len(data)):
            data[i] = min(data[i], data[i-1])
        ax.plot([i*int(60/len(data))*127 for i in range(len(data))], data)
    ax.grid()
    plt.xlabel('Iterations', size=12)
    plt.ylabel('Cost', size=12)
    plt.title(title, size=32)
    plt.show()


def process_tsp_problem(tsp_name, process_file=True):
    if process_file:
        process_and_save_single_results(tsp_name)
    single_results = load_result_file("_single", tsp_name)
    sorted_single = sort_results(single_results)
    print(f'Single instance min value {min(sorted_single[0][1])}')
    #     plot_one_type_results('Single instance', sorted_single[:2])

    if process_file:
        process_and_save_island_model_results(tsp_name, False)
    island_model_2_results = load_result_file("", tsp_name)
    sorted_island_model_2 = sort_results(island_model_2_results)
    print(f'Island Model 2 min value {min(sorted_island_model_2[0][1])}')
    plot_and_compare("Island Model 2 vs Single Instance", sorted_single[:2], sorted_island_model_2[:5])

    if process_file:
        process_and_save_island_model_results(tsp_name, True)
    island_model_3_results = load_result_file("_3islands", tsp_name)
    sorted_island_model_3 = sort_results(island_model_3_results)
    print(f'Island Model 3 min value {min(sorted_island_model_3[0][1])}')
    plot_and_compare("Island Model 3 vs Single Instance", sorted_single[:2], sorted_island_model_3[:5])

    return sorted_single[0], sorted_island_model_2[0], sorted_island_model_3[0]

