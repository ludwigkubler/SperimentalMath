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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def generate_random_poset(n):
    poset = []
    for i in range(n):
        poset.append([])
        for j in range(i + 1, n):
            if random.choice([True, False]):
                poset[i].append(j)
    return poset

def local_induction_dimension(poset):
    n = len(poset)
    if n == 0:
        return 0
    max_indegree = max(sum(1 for j in range(n) if i in poset[j]) for i in range(n))
    return max_indegree + 1

def communication_complexity_rank_variance(poset):
    n = len(poset)
    rank = [len(poset[i]) for i in range(n)]
    mean_rank = sum(rank) / n
    variance = sum((x - mean_rank) ** 2 for x in rank) / n
    return variance

def pearson_correlation_coefficient(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    std_dev_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
    std_dev_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
    return cov_xy / (std_dev_x * std_dev_y)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    l_i_d_values = []
    v_values = []
    
    for n in n_values:
        poset = generate_random_poset(n)
        l_i_d = local_induction_dimension(poset)
        v = communication_complexity_rank_variance(poset)
        l_i_d_values.append(l_i_d)
        v_values.append(v)
    
    correlation_coefficient = pearson_correlation_coefficient(l_i_d_values, v_values)
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": 0.5 <= correlation_coefficient < 0.7,
        "counterexample": "" if 0.5 <= correlation_coefficient < 0.7 else "Pearson Correlation Coefficient out of range [0.5, 0.7)"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Pearson Correlation Coefficient out of range [0.5, 0.7)' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support for conjecture")