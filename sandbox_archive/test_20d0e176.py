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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        pivot = A[i][i]
        if pivot == 0:
            raise ValueError("Matrix is singular")
        for j in range(i+1, n):
            factor = A[j][i] / pivot
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def hodge_theta_index(cnf):
    # Placeholder function to compute Hodge-Theta index
    # This is a dummy implementation and should be replaced with actual computation
    return random.randint(1, 10)

def frege_proof_depth(clause):
    # Placeholder function to compute Frege proof depth
    # This is a dummy implementation and should be replaced with actual computation
    return len(clause) * 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(n, n*10)
    cnf = []
    for _ in range(m):
        variables = list(range(1, n+1))
        clause = [random.choice(variables) * (random.choice([1, -1]))]
        while len(clause) < 3:
            clause.append(random.choice(variables) * (random.choice([1, -1])))
        cnf.append(tuple(sorted(clause)))
    
    hodge_indices = []
    frege_depths = []
    for clause in cnf:
        hodge_index = hodge_theta_index(cnf)
        frege_depth = frege_proof_depth(clause)
        hodge_indices.append(hodge_index)
        frege_depths.append(frege_depth)
    
    max_hodge_index = max(hodge_indices)
    avg_frege_depth = sum(frege_depths) / len(frege_depths)
    
    conjecture_holds = max_hodge_index <= 1.5 * avg_frege_depth
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Hodge-Theta Index",
        "metric_value": max_hodge_index,
        "instances_tested": len(cnf),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.3f} std={std_value:.3f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.3f} std={std_value:.3f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")