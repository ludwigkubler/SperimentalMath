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
    for i in range(n):
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        factor = Fraction(A[i][i])
        for j in range(n):
            A[i][j] /= factor
        for k in range(n):
            if k != i:
                factor = Fraction(A[k][i])
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
    return A

def read_twice_bp_to_noncommutative_crossed_product(bp):
    # Placeholder implementation
    # This is a dummy function to illustrate the structure
    # Replace with actual logic to convert BP to noncommutative crossed product
    E = [[0 for _ in range(len(bp))] for _ in range(len(bp))]
    F = [[0 for _ in range(len(bp))] for _ in range(len(bp))]
    return E, F

def rho(bp):
    E, F = read_twice_bp_to_noncommutative_crossed_product(bp)
    # Placeholder implementation
    # This is a dummy function to illustrate the structure
    # Replace with actual logic to compute the invariant ρ(P)
    return 0.0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    bp = [random.choices([-1, 1], k=n) for _ in range(n)]
    
    metric_value = rho(bp)
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if metric_value > 2 * Fraction(n):
        counterexample = "ρ(P) > 2 * E[ρ(P)]"
    elif abs(metric_value - n) > 0.2 * n:
        counterexample = "ρ(P) deviates by more than 20% from E[ρ(P)]"
    
    if not counterexample:
        conjecture_holds = True
    
    return {
        "metric_name": "ρ(P)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if not r["counterexample"]) / len(results)
    
    if all(not r["counterexample"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(r["metric_value"] > 2 * Fraction(n) for n, r in zip([r["instances_tested"] for r in results], results)):
        first_failing_seed = next(i for i, r in enumerate(results) if r["metric_value"] > 2 * Fraction(r["instances_tested"]))
        print(f"RESULT: FALSIFIED counterexample=\"ρ(P) > 2 * E[ρ(P)]\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")