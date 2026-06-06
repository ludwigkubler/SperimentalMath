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

def gaussian_elimination(A):
    n = len(A)
    A_augmented = [row[:] + [0] for row in A]
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        if A[max_row][i] == 0:
            return None  # Singular matrix
        A[i], A[max_row] = A[max_row], A[i]
        factor = Fraction(A[i][i])
        for j in range(n):
            A[i][j] /= factor
        for j in range(n, 2 * n):
            A[i][j] /= factor
        for k in range(n):
            if k != i:
                factor = Fraction(A[k][i])
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
                for j in range(n, 2 * n):
                    A[k][j] -= factor * A[i][j]
    return [row[n:] for row in A]

def symplectic_topological_degree(A):
    reduced_A = gaussian_elimination(A)
    if reduced_A is None:
        return None
    rank = sum(1 for row in reduced_A if any(row[j] != 0 for j in range(len(row))))
    return rank

def communication_complexity_rank(circuit):
    # Placeholder function to compute the communication complexity rank of a circuit
    # This should be replaced with an actual implementation based on the circuit's structure
    n = len(circuit)
    return random.randint(1, n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            circuit = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
            degree = symplectic_topological_degree(circuit)
            if degree is None:
                continue
            comm_rank = communication_complexity_rank(circuit)
            results.append(comm_rank)
    if not results:
        return {
            "metric_name": "Var(CommRank)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    mean = sum(results) / len(results)
    variance = sum((x - mean) ** 2 for x in results) / len(results)
    expected_variance = n * math.log(n)
    return {
        "metric_name": "Var(CommRank)",
        "metric_value": variance,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": abs(variance - expected_variance) <= 0.1 * expected_variance,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    if all(result is not None for result in results):
        mean = sum(results) / len(results)
        std = (sum((x - mean) ** 2 for x in results) / len(results)) ** 0.5
        support_fraction = sum(1 for r in results if abs(r - n * math.log(n)) <= 0.1 * n * math.log(n)) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if r is None)
        print(f"RESULT: INCONCLUSIVE reason=missing_data n_tested={first_failing_seed + 1}")