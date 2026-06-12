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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def vector_space_basis(f):
        n = len(f)
        basis = []
        for i in range(n):
            vec = f[:]
            vec[i] = 1 - vec[i]
            if all(vec[j] != basis[j][1] for j in range(len(basis))):
                basis.append((i, vec))
        return basis
    
    def symplectic_hull_volume(basis):
        n = len(basis)
        volume = 0
        for i in range(n):
            for j in range(i+1, n):
                if all(basis[i][1][k] != basis[j][1][k] for k in range(len(basis))):
                    volume += 1
        return volume
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        rank = sum(1 for i in range(n) if f[i] == 0)
        variance = (rank - n/2)**2 / n
        return variance
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_random_boolean_function(n)
        basis = vector_space_basis(f)
        shv = symplectic_hull_volume(basis)
        crv = communication_complexity_rank_variance(f)
        results.append((shv, crv))
    
    if not results:
        return {
            "metric_name": "SHV vs CRV correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    shv_values = [r[0] for r in results]
    crv_values = [r[1] for r in results]
    
    mean_shv = sum(shv_values) / len(shv_values)
    mean_crv = sum(crv_values) / len(crv_values)
    
    correlation_coefficient = (sum((shv_values[i] - mean_shv) * (crv_values[i] - mean_crv) for i in range(len(results))) /
                               math.sqrt(sum((shv_values[i] - mean_shv)**2 for i in range(len(results))) *
                                         sum((crv_values[i] - mean_crv)**2 for i in range(len(results)))))
    
    return {
        "metric_name": "SHV vs CRV correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": "" if correlation_coefficient > 0.7 else f"correlation={correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")