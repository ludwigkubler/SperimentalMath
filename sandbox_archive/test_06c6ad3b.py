# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def generate_instance(n):
    return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]

def local_coherence_index(configuration_space):
    n = len(configuration_space)
    sum_i = sum(configuration_space[i][i] for i in range(n))
    sum_ij = sum(configuration_space[i][j] + configuration_space[j][i] for i in range(n) for j in range(i+1, n))
    return Fraction(sum_i, sum_ij)

def median(lst):
    sorted_lst = sorted(lst)
    n = len(sorted_lst)
    if n % 2 == 0:
        return (sorted_lst[n//2 - 1] + sorted_lst[n//2]) / 2
    else:
        return sorted_lst[n//2]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 40:
            continue
        instance = generate_instance(n)
        I = local_coherence_index(instance)
        V = sum(sum(row) for row in instance)
        R = median([sum(row) for row in instance])
        if R == 0:
            continue
        ratio = Fraction(V, R)
        results.append((I, ratio))
    
    if not results:
        return {
            "metric_name": "local_coherence_index_ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    I_values = [I for I, _ in results]
    ratio_values = [ratio for _, ratio in results]
    mean_I = sum(I_values) / len(I_values)
    mean_ratio = sum(ratio_values) / len(ratio_values)
    std_dev_I = math.sqrt(sum((I - mean_I)**2 for I in I_values) / len(I_values))
    std_dev_ratio = math.sqrt(sum((ratio - mean_ratio)**2 for ratio in ratio_values) / len(ratio_values))
    
    return {
        "metric_name": "local_coherence_index_ratio",
        "metric_value": mean_I,
        "instances_tested": len(results),
        "n_max": max([len(instance) for instance, _ in results]),
        "conjecture_holds": abs(mean_I - mean_ratio) < 0.1 * (mean_I + mean_ratio),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_dev_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")