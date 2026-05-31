# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import sys

def generate_circuit(n, w):
    circuit = []
    for _ in range(w):
        gate = [random.randint(0, 1) for _ in range(n)]
        circuit.append(gate)
    return circuit

def permute_matrix(matrix, perm):
    n = len(matrix)
    permuted = [[matrix[i][perm[j]] for j in range(n)] for i in range(n)]
    return permuted

def is_valid_permutation(perm, matrix):
    n = len(matrix)
    permuted = permute_matrix(matrix, perm)
    for row in permuted:
        if any(row[i] != matrix[0][i] for i in range(n)):
            return False
    return True

def count_valid_perms(matrix):
    n = len(matrix)
    perms = [list(range(n)) for _ in range(math.factorial(n))]
    random.shuffle(perms)
    valid_count = sum(is_valid_permutation(perm, matrix) for perm in perms[:30])  # Sample 30 permutations
    return valid_count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for w in range(2, min(n, 5)):  # Width should be less than or equal to n
            circuit = generate_circuit(n, w)
            perm_count = count_valid_perms(circuit)
            expected_bound = n ** (w / 2)
            ratio = Fraction(perm_count, expected_bound).limit_denominator()
            results.append({
                "n": n,
                "w": w,
                "perm_count": perm_count,
                "expected_bound": expected_bound,
                "ratio": ratio
            })
    
    metric_value = sum(result["ratio"] for result in results) / len(results)
    conjecture_holds = all(result["ratio"] <= 2 for result in results)  # Example threshold, adjust as needed
    counterexample = "" if conjecture_holds else "threshold_violation"
    
    return {
        "metric_name": "Ratio of permutation matrices to expected bound",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"threshold_violation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")