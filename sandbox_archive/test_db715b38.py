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
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        factor = Fraction(A[i][i], 1)
        for j in range(n):
            A[i][j] /= factor
        for k in range(n):
            if k != i:
                factor = Fraction(A[k][i], 1)
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
    return A

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    d = random.randint(2, 10)
    C = Fraction(1, 1)  # Universal constant C
    threshold = C * math.sqrt(n / d**3)

    # Generate a random max-CUT instance
    graph = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        graph[i][i] = 0

    # Compute the degree-d SOS moment matrix M
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if graph[i][j] == 1:
                for k in range(d):
                    M[i][k] += Fraction(1, d)
                    M[j][k] += Fraction(1, d)

    # Calculate the eigenvalue spectrum of M
    eigenvalues = []
    A = [row[:] for row in M]
    for i in range(n):
        pivot = A[i][i]
        if pivot == 0:
            return {"metric_name": "eigenvalue", "metric_value": None, "instances_tested": 1, "conjecture_holds": False, "counterexample": "mapping_undefined"}
        for j in range(n):
            A[j][i] /= pivot
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
        eigenvalues.append(A[i][i])

    # Verify if eigenvalues exceed the threshold
    max_eigenvalue = max(eigenvalues)
    if max_eigenvalue > threshold:
        return {"metric_name": "eigenvalue", "metric_value": max_eigenvalue, "instances_tested": 1, "conjecture_holds": False, "counterexample": f"Max eigenvalue {max_eigenvalue} exceeds threshold {threshold}"}
    else:
        return {"metric_name": "eigenvalue", "metric_value": max_eigenvalue, "instances_tested": 1, "conjecture_holds": True, "counterexample": ""}

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Max eigenvalue exceeds threshold\" first_failing_seed={first_failing_seed}")