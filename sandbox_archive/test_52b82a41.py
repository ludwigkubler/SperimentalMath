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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = len(f)
        rank = 0
        for i in range(n):
            for j in range(i + 1, n):
                if f[i] != f[j]:
                    rank += 1
        return rank
    
    def lie_algebra_from_function(f):
        n = len(f)
        ideals = []
        for i in range(2**n):
            ideal = [f[(i >> j) & 1] for j in range(n)]
            if all(ideal[j] == ideal[(j + k) % n] for k in range(n)):
                ideals.append(ideal)
        return ideals
    
    def coadjointness_index(ideals):
        n = len(ideals[0])
        index = 0
        for ideal in ideals:
            for j in range(n):
                if all(ideal[j] == ideal[(j + k) % n] for k in range(n)):
                    index += 1
        return index
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x)))
        var_x = sum((x[i] - mean_x)**2 for i in range(len(x)))
        var_y = sum((y[i] - mean_y)**2 for i in range(len(y)))
        return cov_xy / math.sqrt(var_x * var_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        r_f = communication_complexity_rank(f)
        ideals = lie_algebra_from_function(f)
        index = coadjointness_index(ideals)
        results.append((r_f, index))
    
    if not results:
        return {
            "metric_name": "coadjointness_index",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    r_f_values, index_values = zip(*results)
    corr = pearson_correlation(r_f_values, index_values)
    
    return {
        "metric_name": "coadjointness_index",
        "metric_value": corr,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(corr) > 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['instances_tested']}, corr={r['metric_value']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break