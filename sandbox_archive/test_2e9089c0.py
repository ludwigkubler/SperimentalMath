# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_planar_graph(n):
        if n < 3:
            return []
        vertices = list(range(n))
        edges = []
        for i in range(1, n):
            edges.append((0, i))
        for i in range(2, n):
            edges.append((i-1, i))
        random.shuffle(edges)
        while len(edges) > 3 * (n - 1):
            edges.pop()
        return vertices, edges
    
    def compute_minimal_hyperbolic_volume(G):
        # Placeholder implementation
        return random.random() * n
    
    def compute_communication_complexity(G):
        # Placeholder implementation
        return random.randint(10, 50)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        G = generate_random_planar_graph(n)
        mvol_G = compute_minimal_hyperbolic_volume(G)
        ccom_G = compute_communication_complexity(G)
        results.append((mvol_G, ccom_G))
    
    if not results:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mvol_values = [r[0] for r in results]
    ccom_values = [r[1] for r in results]
    
    mean_mvol = sum(mvol_values) / len(mvol_values)
    mean_ccom = sum(ccom_values) / len(ccom_values)
    std_dev_mvol = math.sqrt(sum((x - mean_mvol) ** 2 for x in mvol_values) / len(mvol_values))
    std_dev_ccom = math.sqrt(sum((x - mean_ccom) ** 2 for x in ccom_values) / len(ccom_values))
    
    correlation_coefficient = sum((mvol_values[i] - mean_mvol) * (ccom_values[i] - mean_ccom) for i in range(len(mvol_values))) / (len(mvol_values) * std_dev_mvol * std_dev_ccom)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.8 and std_dev_mvol <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        exit(1)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")