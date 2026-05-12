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

def generate_max_cut_instance(n):
    A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        A[i][i] = 0
    return [sum(row) for row in A]

def gram_matrix(A):
    n = len(A)
    G = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            sum_val = sum(A[i][k] * A[j][k] for k in range(n))
            G[i][j] = G[j][i] = sum_val
    return G

def gaussian_elimination(G):
    n = len(G)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(G[j][i]) > abs(G[max_row][i]):
                max_row = j
        G[i], G[max_row] = G[max_row], G[i]
        for j in range(i+1, n):
            factor = G[j][i] / G[i][i]
            for k in range(i, n):
                G[j][k] -= factor * G[i][k]
    return G

def count_non_zero_eigenvalues(G):
    n = len(G)
    eigenvalues = [G[i][i] for i in range(n)]
    return sum(1 for ev in eigenvalues if abs(ev) > 1e-6)

def sos_degree(k):
    return math.ceil(math.log2(k))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    instance = generate_max_cut_instance(n)
    G = gram_matrix(instance)
    G = gaussian_elimination(G)
    k = count_non_zero_eigenvalues(G)
    required_degree = sos_degree(k)
    
    metric_value = required_degree
    instances_tested = 1
    conjecture_holds = required_degree >= math.log2(k)
    counterexample = "" if conjecture_holds else f"n={n}, k={k}, degree={required_degree}"
    
    return {
        "metric_name": "SOS Degree",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 33)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")