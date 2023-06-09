tsp_configs = {
    # "aco_1__3": ('aco', {
    #     "alpha": 1,
    #     "beta": 3,
    # }),
    "aco_1__4_2": ('aco', {
        "alpha": 1,
        "beta": 4.2,
    }),
    "ga_9_35_exponential_tournament": ('genetic', {
        "cr": 0.9,
        "param_s": 0.35,
        "crossover": "exponential",
        "selection": "tournament",
    }),
    # "ga_8_6_single_tournament": ('genetic', {
    #     "cr": 0.8,
    #     "param_s": 0.6,
    #     "crossover": "single",
    #     "selection": "tournament",
    # }),
    # "pso_2_05__2_05__1__2__25": ('pso', {
    #     'eta1': 2.05,
    #     'eta2': 2.05,
    #     'variant': 1,
    #     'neighb_type': 2,
    #     'neighb_param': 0.25,
    # }),
    # "pso_2_05__1_3__6__1__4": ('pso', {
    #     'eta1': 2.05,
    #     'eta2': 1.3,
    #     'variant': 6,
    #     'neighb_type': 1,
    #     'neighb_param': 0.4,
    # }),
}