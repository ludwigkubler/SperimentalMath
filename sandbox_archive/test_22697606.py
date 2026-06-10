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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(i, n + 1):
                A[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(i, n + 1):
                        A[j][k] -= factor * A[i][k]
        return A

    def determinant(A):
        n = len(A)
        det = 1
        for i in range(n):
            det *= A[i][i]
        return det

    def hyperbolic_volume(n):
        # Generate a random n-bit Boolean function
        boolean_function = [random.choice([0, 1]) for _ in range(2**n)]
        
        # Create the adjacency matrix for the Poincaré disk model
        A = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(i+1, 2**n):
                if boolean_function[i] != boolean_function[j]:
                    A[i][j] = 1
                    A[j][i] = 1
        
        # Compute the hyperbolic volume using the determinant of the adjacency matrix
        det = determinant(gaussian_elimination(A))
        return abs(det) ** (1/n)

    n_values = [5, 10, 15, 20, 30, 40]
    volumes = []
    for n in n_values:
        volume = hyperbolic_volume(n)
        volumes.append(volume)
    
    mean_volume = sum(volumes) / len(volumes)
    conjecture_holds = all(0.5 <= v / (1/math.sqrt(n)) <= 2 for n, v in zip(n_values, volumes))
    counterexample = "" if conjecture_holds else "volume_out_of_bounds"
    
    return {
        "metric_name": "Hyperbolic Volume",
        "metric_value": mean_volume,
        "instances_tested": len(volumes),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"volume_out_of_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")