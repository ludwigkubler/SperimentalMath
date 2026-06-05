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
    
    def convex_hull_lattice_points(f):
        n = len(f)
        points = [(i & (1 << j)) for i in range(2**n) for j in range(n)]
        hull = set()
        for point in points:
            if all(point[i] <= f[point[i]] for i in range(n)):
                hull.add(tuple(sorted(point)))
        return len(hull)
    
    def matrix_representation(f):
        n = len(f)
        A = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if all((i & (1 << k)) <= f[(j & (1 << k))] for k in range(n)):
                    A[i][j] = 1
        return A
    
    def rank_of_matrix(A):
        n = len(A)
        m = len(A[0])
        M = [A[i] + [-i] for i in range(n)]
        r = 0
        for j in range(m):
            if all(M[i][j] == 0 for i in range(r, n)):
                continue
            pivot_row = r
            while M[pivot_row][j] == 0:
                pivot_row += 1
                if pivot_row == n:
                    break
            M[pivot_row], M[r] = M[r], M[pivot_row]
            for i in range(r + 1, n):
                factor = -M[i][j] / M[r][j]
                for k in range(m):
                    M[i][k] += factor * M[r][k]
            r += 1
        return r
    
    def generate_random_integers(k):
        return [random.randint(0, 2**31 - 1) for _ in range(k)]
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_points = 0
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            points = convex_hull_lattice_points(f)
            A = matrix_representation(f)
            rank = rank_of_matrix(A)
            total_points += points
            total_rank += rank
            instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "lattice_point_count_to_rank_ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    ratio = total_points / total_rank
    if ratio > 1.5:
        return {
            "metric_name": "lattice_point_count_to_rank_ratio",
            "metric_value": ratio,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"ratio={ratio} exceeds 1.5"
        }
    
    return {
        "metric_name": "lattice_point_count_to_rank_ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and "counterexample" in r for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if "counterexample" in result)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")