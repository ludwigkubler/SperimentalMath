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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def matrix_representation(f):
        n = int(math.log2(len(f)))
        M = []
        for i in range(2**n):
            row = [f[i >> j & 1] for j in range(n)]
            M.append(row)
        return M
    
    def rank_of_matrix(M):
        m, n = len(M), len(M[0])
        if m == 0 or n == 0:
            return 0
        A = M.copy()
        lead = 0
        for r in range(m):
            if lead >= n:
                break
            i = r
            while A[i][lead] == 0:
                i += 1
                if i == m:
                    i = r
                    lead += 1
                    if lead == n:
                        return 0
            A[r], A[i] = A[i], A[r]
            for i in range(m):
                if i != r:
                    factor = -A[i][lead] / A[r][lead]
                    for j in range(n):
                        A[i][j] += factor * A[r][j]
        return sum(1 for row in A if any(row))
    
    def convex_hull_lattice_points(M):
        n = len(M[0])
        lattice_points = 0
        for i in range(2**n):
            point = [i >> j & 1 for j in range(n)]
            valid = True
            for row in M:
                if all(point[j] <= row[j] for j in range(n)):
                    lattice_points += 1
                    break
        return lattice_points
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_lattice_points = 0
    total_rank = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        f = generate_boolean_function(n)
        M = matrix_representation(f)
        rank = rank_of_matrix(M)
        lattice_points = convex_hull_lattice_points(M)
        
        if lattice_points is None or rank is None:
            return {
                "metric_name": "Lattice Point Count / Rank Ratio",
                "metric_value": float('nan'),
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        total_lattice_points += lattice_points
        total_rank += rank
        instances_tested += 1
        n_max = max(n_max, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "Lattice Point Count / Rank Ratio",
            "metric_value": float('nan'),
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    ratio = total_lattice_points / total_rank
    if ratio > 1.5:
        return {
            "metric_name": "Lattice Point Count / Rank Ratio",
            "metric_value": ratio,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"Ratio {ratio} exceeds 1.5"
        }
    
    return {
        "metric_name": "Lattice Point Count / Rank Ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=nan support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")