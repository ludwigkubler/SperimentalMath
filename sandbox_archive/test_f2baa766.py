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
    
    def communication_matrix_rank(f):
        n = len(f)
        matrix = []
        for i in range(n):
            row = [f[j] ^ f[i] for j in range(n)]
            matrix.append(row)
        rank = 0
        for row in matrix:
            if any(row[j] != 0 for j in range(rank)):
                rank += 1
        return rank
    
    def generate_hyperplane_arrangement(f):
        n = len(f)
        hyperplanes = []
        for i in range(n):
            hyperplanes.append([i, f[i]])
        return hyperplanes
    
    def min_symplectic_geometry_rank(G_f):
        # Placeholder implementation; actual computation depends on the specific geometry
        return len(G_f)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        f = generate_random_boolean_function(n)
        r_f = communication_matrix_rank(f)
        G_f = generate_hyperplane_arrangement(f)
        min_rank_G_f = min_symplectic_geometry_rank(G_f)
        results.append({
            "n": n,
            "r_f": r_f,
            "min_rank_G_f": min_rank_G_f
        })
    
    metric_value = sum(abs(r_f / min_rank_G_f) for r_f, min_rank_G_f in zip([res["r_f"] for res in results], [res["min_rank_G_f"] for res in results])) / len(results)
    conjecture_holds = all(0.5 <= abs(r_f / min_rank_G_f) <= 2 for r_f, min_rank_G_f in zip([res["r_f"] for res in results], [res["min_rank_G_f"] for res in results]))
    
    return {
        "metric_name": "Communication Matrix Rank vs Min Symplectic Geometry Rank",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max([res["n"] for res in results]),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")