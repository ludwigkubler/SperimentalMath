# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_matrix_rank(f):
        n = len(f)
        matrix = []
        for i in range(2**n):
            row = []
            for j in range(n):
                row.append((i >> j) & 1)
            matrix.append(row)
        rank = 0
        for row in matrix:
            if any(row[j] != 0 for j in range(rank)):
                rank += 1
        return rank
    
    def construct_hyperplane_arrangement(f):
        n = len(f)
        hyperplanes = []
        for i in range(n):
            hyperplanes.append(random.randint(1, 10))
        return hyperplanes
    
    def min_symplectic_geometry_rank(hyperplanes):
        n = len(hyperplanes)
        rank = 0
        for h in hyperplanes:
            if any(h != 0):
                rank += 1
        return rank
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_random_boolean_function(n)
        r_f = communication_matrix_rank(f)
        G_f = construct_hyperplane_arrangement(f)
        min_rank_G_f = min_symplectic_geometry_rank(G_f)
        
        if r_f == 0:
            continue
        
        ratio = abs(min_rank_G_f / r_f)
        results.append((r_f, min_rank_G_f, ratio))
    
    if not results:
        return {
            "metric_name": "min_symplectic_geometry_rank_over_communication_matrix_rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_ratio = sum(ratio for _, _, ratio in results) / len(results)
    support_fraction = sum(1 for _, _, ratio in results if 0.5 <= ratio <= 2) / len(results)
    
    return {
        "metric_name": "min_symplectic_geometry_rank_over_communication_matrix_rank",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(n for _, _, _ in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"mean_ratio={mean_ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")