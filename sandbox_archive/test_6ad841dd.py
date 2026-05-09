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

def gram_schmidt(monomials):
    n = len(monomials)
    Q = []
    for i in range(n):
        q_i = monomials[i]
        for j in range(i):
            q_j = Q[j]
            proj = sum(q_i[k] * q_j[k] for k in range(len(q_i))) / sum(q_j[k]**2 for k in range(len(q_j)))
            q_i = [q_i[k] - proj * q_j[k] for k in range(len(q_i))]
        norm = math.sqrt(sum(q_i[k]**2 for k in range(len(q_i))))
        Q.append([q_i[k] / norm for k in range(len(q_i))])
    return Q

def moment_matrix(monomials, d):
    n = len(monomials)
    M = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(n):
            if abs(monomials[i][j]) > 1e-9:
                M[i][j] = monomials[i][j]
                M[j][i] = monomials[j][i]
    return M

def count_non_zero_entries(matrix):
    n = len(matrix)
    count = 0
    for i in range(n):
        for j in range(i, n):
            if matrix[i][j] != 0:
                count += 1
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    d = random.randint(2, 5)
    
    # Generate a random Max-CUT instance
    variables = [f'x{i}' for i in range(n)]
    monomials = []
    for i in range(n):
        for j in range(i + 1, n):
            monomials.append([0] * (n + 1))
            monomials[-1][i] = random.choice([-1, 1])
            monomials[-1][j] = random.choice([-1, 1])
    
    # Construct the degree-d moment matrix
    Q = gram_schmidt(monomials)
    M = moment_matrix(Q, d)
    
    # Count non-zero entries in the moment matrix
    non_zero_count = count_non_zero_entries(M)
    
    # Calculate the sparsity threshold
    sparsity_threshold = n**2 / (d**2 * 4)  # Θ(n²/d²) is an overestimate for simplicity
    
    # Check if the conjecture holds
    conjecture_holds = non_zero_count >= sparsity_threshold
    
    return {
        "metric_name": "non_zero_entries",
        "metric_value": non_zero_count,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, d={d}, non_zero_count={non_zero_count}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    # Compute mean/std of metric_value and fraction of seeds where conjecture_holds
    total_non_zero_entries = sum(r["metric_value"] for r in results)
    total_instances_tested = sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    mean_non_zero_entries = total_non_zero_entries / total_instances_tested
    std_non_zero_entries = math.sqrt(sum((r["metric_value"] - mean_non_zero_entries)**2 for r in results) / total_instances_tested)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_non_zero_entries} std={std_non_zero_entries} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")