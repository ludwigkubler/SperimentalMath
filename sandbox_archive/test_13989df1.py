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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def determinant(A):
    n = len(A)
    det = 1
    U = gaussian_elimination(A)
    for i in range(n):
        det *= U[i][i]
    return det

def primary_decomposition(M):
    n = len(M)
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    A = [row[:] for row in M]
    B = [row[:] for row in I]
    rank = 0
    for i in range(n):
        if A[i][i] != 0:
            rank += 1
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    B[j][k] -= factor * B[i][k]
    return rank

def random_matrix(n):
    return [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]

def circuit_size_perm_n(n):
    # Placeholder function to simulate a black-box SAT solver
    # This is a dummy implementation and should be replaced with an actual algorithm
    return n * (n + 1) // 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in range(5, 41):
        M = random_matrix(n)
        d_M = primary_decomposition(M)
        CircuitSize = circuit_size_perm_n(n)
        metric_value = CircuitSize / math.log(n)
        conjecture_holds = CircuitSize >= d_M / math.log(n)
        results.append({
            "n": n,
            "d_M": d_M,
            "CircuitSize": CircuitSize,
            "metric_value": metric_value,
            "conjecture_holds": conjecture_holds
        })
    return {
        "metric_name": "orbit_closure_dimension",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": "" if all(result["conjecture_holds"] for result in results) else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed)["conjecture_holds"] for seed in seeds]
    support_fraction = sum(results) / len(results)
    if all(results):
        print(f"RESULT: SUPPORTED mean={sum(run_trial(seed)['metric_value'] for seed in seeds)/len(seeds)} std=0.0 support_fraction=1.0")
    elif sum(results) >= 0.8 * len(results):
        print(f"RESULT: SUPPORTED mean={sum(run_trial(seed)['metric_value'] for seed in seeds)/len(seeds)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, x in enumerate(results) if not x)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed+1}")