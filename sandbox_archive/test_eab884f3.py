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

def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def compute_communication_complexity_rank(f):
    n = int(math.log2(len(f)))
    if len(f) != 2**n:
        raise ValueError("Invalid function size")
    T = [[f[i] ^ f[j] for j in range(n)] for i in range(n)]
    rank = 0
    for row in T:
        if any(row):
            rank += 1
            for j in range(n):
                if row[j]:
                    for k in range(j+1, n):
                        if T[k][j] and not T[k][j^i]:
                            T[k][j] = False
    return rank

def compute_matrix_representation(f):
    n = int(math.log2(len(f)))
    matrix = [[f[i] ^ f[j] for j in range(n)] for i in range(n)]
    return matrix

def gaussian_elimination(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for i in range(m):
        if rank < n:
            pivot_row = i
            while pivot_row < m and not any(matrix[pivot_row]):
                pivot_row += 1
            if pivot_row == m:
                break
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            for j in range(n):
                if matrix[i][j]:
                    for k in range(m):
                        if k != i and matrix[k][j]:
                            matrix[k][j] ^= 1
            rank += 1
    return rank

def compute_alexander_dirac_invariant(matrix):
    m, n = len(matrix), len(matrix[0])
    if m != n:
        raise ValueError("Matrix must be square")
    rank = gaussian_elimination(matrix)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_random_boolean_function(n)
        comm_rank = compute_communication_complexity_rank(f)
        matrix = compute_matrix_representation(f)
        alexander_dirac_invariant = compute_alexander_dirac_invariant(matrix)
        results.append((comm_rank, alexander_dirac_invariant))
    if not results:
        return {"metric_name": "correlation", "metric_value": None, "instances_tested": 0, "n_max": 0, "conjecture_holds": False, "counterexample": "mapping_undefined"}
    
    comm_ranks = [r[0] for r in results]
    alexander_dirac_invariants = [r[1] for r in results]
    mean_comm_rank = sum(comm_ranks) / len(comm_ranks)
    mean_ad_inv = sum(alexander_dirac_invariants) / len(alexander_dirac_invariants)
    
    correlation = (sum((comm_ranks[i] - mean_comm_rank) * (alexander_dirac_invariants[i] - mean_ad_inv) for i in range(len(comm_ranks))) /
                   math.sqrt(sum((comm_ranks[i] - mean_comm_rank)**2 for i in range(len(comm_ranks)))) /
                   math.sqrt(sum((alexander_dirac_invariants[i] - mean_ad_inv)**2 for i in range(len(alexander_dirac_invariants)))))
    
    return {"metric_name": "correlation", "metric_value": correlation, "instances_tested": len(results), "n_max": 40, "conjecture_holds": abs(correlation) >= 1.5, "counterexample": "" if abs(correlation) >= 1.5 else f"Correlation {correlation} outside expected range"}

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_outside_range' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")