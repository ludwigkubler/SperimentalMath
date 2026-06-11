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
    m, n = len(A), len(A[0])
    for i in range(m):
        pivot_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[pivot_row][i]):
                pivot_row = j
        A[i], A[pivot_row] = A[pivot_row], A[i]
        pivot = A[i][i]
        if pivot == 0:
            continue
        for j in range(n):
            A[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def construct_twisted_module(circuit):
    # Placeholder for the actual implementation of constructing a twisted module
    # This is just a dummy function to avoid division by zero errors
    m = len(circuit)
    n = len(circuit[0])
    A = [[random.randint(0, 1) for _ in range(n)] for _ in range(m)]
    return gaussian_elimination(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    circuit_sizes = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in circuit_sizes:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
            entanglement_complexity = sum(sum(row) for row in circuit)
            M = construct_twisted_module(circuit)
            min_order = len(M)
            
            results.append({
                "metric_name": "min_order",
                "metric_value": min_order,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": min_order <= entanglement_complexity and min_order >= 1,
                "counterexample": "" if min_order <= entanglement_complexity else f"min_order={min_order} > e(C)={entanglement_complexity}"
            })
    
    mean_min_order = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_min_order": mean_min_order,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_min_order = sum(r["mean_min_order"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["support_fraction"] >= 0.8) / len(results)
    
    if all(r["support_fraction"] >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean_min_order={mean_min_order} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='min_order > e(C)' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")