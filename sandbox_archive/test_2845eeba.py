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
    
    def gram_schmidt_process(vectors):
        n = len(vectors)
        u = [v[:] for v in vectors]
        norms = [math.sqrt(sum(x * x for x in v)) for v in u]
        for i in range(n):
            u[i] = [x / norm for x, norm in zip(u[i], norms)]
            for j in range(i + 1, n):
                proj = sum(u[j][k] * u[i][k] for k in range(len(vectors[0])))
                u[j] = [u[j][k] - proj * u[i][k] for k in range(len(vectors[0]))]
        return u
    
    def frobenius_schmidt_distance(state, uniform):
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(state, uniform)))
    
    def communication_complexity_rank_variance(f, n):
        instances = [f(x) for x in range(2**n)]
        rank = len(set(instances))
        return rank / (2**n)
    
    def spearman_rho(correlations):
        n = len(correlations)
        ranks = {x: i + 1 for i, x in enumerate(sorted(correlations))}
        rho_numerator = sum((ranks[x] - ranks[y]) ** 2 for x, y in zip(correlations, sorted(correlations)))
        rho_denominator = (n * (n**2 - 1)) / 6
        return 1 - (6 * rho_numerator) / rho_denominator
    
    n_values = [5, 10, 15, 20, 30, 40]
    fs_dist_values = []
    ccr_var_values = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        state = gram_schmidt_process([f(x) for x in range(2**n)])
        uniform = [1 / (2**n)] * len(state)
        fs_dist = frobenius_schmidt_distance(state, uniform)
        ccr_var = communication_complexity_rank_variance(f, n)
        
        fs_dist_values.append(fs_dist)
        ccr_var_values.append(ccr_var)
    
    correlation = spearman_rho([fs_dist * ccr_var for fs_dist, ccr_var in zip(fs_dist_values, ccr_var_values)])
    
    return {
        "metric_name": "Spearman's rho",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.5,
        "counterexample": "" if correlation >= 0.5 else "Spearman's rho < 0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Spearman's rho < 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")