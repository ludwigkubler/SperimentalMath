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
    
    def frobenius_schmidt_distance(state, uniform_dist):
        n = len(state)
        diff = [state[i] - uniform_dist[i] for i in range(n)]
        norm_diff = sum(x * x.conjugate() for x in diff) ** 0.5
        norm_uniform = sum(uniform_dist[i] * uniform_dist[i].conjugate() for i in range(n)) ** 0.5
        return norm_diff / norm_uniform
    
    def communication_complexity_rank_variance(f, n):
        instances = [f(x) for x in range(2**n)]
        rank_var = sum(instances.count(i) for i in set(instances))
        return rank_var / len(instances)
    
    def gram_schmidt_process(vectors):
        n = len(vectors)
        q = []
        e = []
        for v in vectors:
            e.append(v)
            for u in q:
                proj_u_v = sum(u[i] * v[i].conjugate() for i in range(n)) / sum(u[i] * u[i].conjugate() for i in range(n))
                e[-1][i] -= proj_u_v * u[i]
            norm_e = sum(e[-1][i] * e[-1][i].conjugate() for i in range(n)) ** 0.5
            q.append([e[-1][i] / norm_e for i in range(n)])
        return q
    
    def uniform_distribution(n):
        return [Fraction(1, 2**n)] * (2**n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    fs_dist_sum = 0
    ccr_var_sum = 0
    instances_tested = 0
    
    for n in n_values:
        f = generate_boolean_function(n)
        state = gram_schmidt_process([f(x) for x in range(2**n)])
        uniform_dist = uniform_distribution(n)
        fs_dist = frobenius_schmidt_distance(state, uniform_dist)
        ccr_var = communication_complexity_rank_variance(f, n)
        
        fs_dist_sum += fs_dist
        ccr_var_sum += ccr_var
        instances_tested += 2**n
    
    mean_fs_dist = fs_dist_sum / len(n_values)
    mean_ccr_var = ccr_var_sum / len(n_values)
    
    if mean_fs_dist == 0 or mean_ccr_var == 0:
        return {
            "metric_name": "FS_dist vs CCR_var",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    rho = (mean_fs_dist * mean_ccr_var - sum(frobenius_schmidt_distance(state, uniform_dist) * communication_complexity_rank_variance(f, n) for state in gram_schmidt_process([f(x) for x in range(2**n)]) for f in [generate_boolean_function(n)] for n in n_values)) / (math.sqrt(sum((frobenius_schmidt_distance(state, uniform_dist) - mean_fs_dist)**2 for state in gram_schmidt_process([f(x) for x in range(2**n)]) for f in [generate_boolean_function(n)] for n in n_values)) * math.sqrt(sum((communication_complexity_rank_variance(f, n) - mean_ccr_var)**2 for f in [generate_boolean_function(n)] for n in n_values)))
    
    return {
        "metric_name": "FS_dist vs CCR_var",
        "metric_value": rho,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": abs(rho) >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rho is not significantly positive\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")