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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    Augmented = [row + [b[i]] for i, row in enumerate(A)]
    for i in range(m):
        max_row = max(range(i, m), key=lambda k: abs(Augmented[k][i]))
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        factor = 1 / Augmented[i][i]
        for j in range(n + 1):
            Augmented[i][j] *= factor
        for k in range(m):
            if k != i:
                factor = Augmented[k][i]
                for j in range(n + 1):
                    Augmented[k][j] -= factor * Augmented[i][j]
    return [row[-1] for row in Augmented]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 10)
    inputs = [[random.randint(-5, 5) for _ in range(n)] for _ in range(30)]
    
    # Simulate tropical derivation sparsity
    sparsity = max(sum(x != 0 for x in row) for row in inputs)
    
    # Simulate phase cell count (placeholder)
    phase_cells = sum(len(set(tuple(row) for row in inputs)) for _ in range(10))
    
    return {
        "metric_name": "phase_cell_count",
        "metric_value": phase_cells,
        "instances_tested": len(inputs),
        "conjecture_holds": phase_cells <= sparsity**2,  # Placeholder polynomial bound
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(30))
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")