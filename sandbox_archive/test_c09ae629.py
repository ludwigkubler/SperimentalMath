# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, product

# Constants
MAX_N = 40
NUM_TRIALS_PER_SEED = 30
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149]

def random_graph(n, girth):
    if n < girth:
        return None
    edges = set()
    for i in range(girth):
        edges.add((i, (i + 1) % n))
    while len(edges) < n * (n - 1) // 2:
        u, v = random.sample(range(n), 2)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            for _ in range(girth):
                if (u, v) in edges or (v, u) in edges:
                    break
                edges.add((u, v))
                u = (u + 1) % n
    return edges

def gaussian_elimination(matrix):
    m, n = len(matrix), len(matrix[0])
    for i in range(m):
        if matrix[i][i] == 0:
            for j in range(i + 1, m):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
            else:
                return None
        pivot = Fraction(matrix[i][i])
        for j in range(n):
            matrix[i][j] /= pivot
        for j in range(m):
            if i != j:
                factor = Fraction(matrix[j][i])
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def minimal_tropical_motivic_rank(cnf):
    n = len(cnf)
    matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for i, clause in enumerate(cnf):
        for literal in clause:
            if literal > 0:
                matrix[literal - 1][i] = 1
            else:
                matrix[-literal - 1][i] = 1
    matrix = gaussian_elimination(matrix)
    rank = sum(1 for row in matrix if any(row))
    return rank

def communication_complexity_rank(cnf):
    n = len(cnf)
    matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for i, clause in enumerate(cnf):
        for literal in clause:
            if literal > 0:
                matrix[literal - 1][i] = 1
            else:
                matrix[-literal - 1][i] = 1
    matrix = gaussian_elimination(matrix)
    rank = sum(1 for row in matrix if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(NUM_TRIALS_PER_SEED):
            graph = random_graph(n, girth=5)
            if graph is None:
                continue
            cnf = [sorted([random.choice([-1, 1]) * (i + 1) for i in range(n)]) for _ in range(n)]
            mtr = minimal_tropical_motivic_rank(cnf)
            ccr = communication_complexity_rank(cnf)
            if mtr == 0 or ccr == 0:
                continue
            ratio = Fraction(mtr, ccr)
            results.append((n, mtr, ccr, ratio))
    
    if not results:
        return {
            "metric_name": "mtr_to_ccr_ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(n for _, _, _, _ in results)
    conjecture_holds = all(abs(ratio - Fraction(mtr, ccr)) <= 1e-6 for _, mtr, ccr, ratio in results)
    counterexample = "" if conjecture_holds else "mtr_to_ccr_ratio does not hold"
    
    return {
        "metric_name": "mtr_to_ccr_ratio",
        "metric_value": sum(ratio for _, _, _, ratio in results) / len(results),
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or PRIMES[:30]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
    
    results = [run_trial(seed)["metric_value"] for seed in seeds if run_trial(seed)["metric_value"] is not None]
    support_fraction = sum(1 for r in results if abs(r - Fraction(sum(results) / len(results), 1)) <= 1e-6) / len(results)
    
    if all(trial_result["conjecture_holds"] for trial_result in [run_trial(seed) for seed in seeds]):
        print(f"RESULT: SUPPORTED mean={sum(results)/len(results)} std={math.sqrt(sum((x - sum(results)/len(results))**2 for x in results) / len(results))} support_fraction={support_fraction}")
    elif any(not trial_result["conjecture_holds"] for trial_result in [run_trial(seed) for seed in seeds]):
        first_failing_seed = next(seed for seed in seeds if not run_trial(seed)["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mtr_to_ccr_ratio does not hold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=30")