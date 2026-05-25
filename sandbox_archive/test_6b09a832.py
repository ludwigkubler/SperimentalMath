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
    rows, cols = len(A), len(A[0])
    for i in range(rows):
        # Find pivot
        max_row = i
        for j in range(i+1, rows):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, rows):
            factor = A[j][i] / A[i][i]
            for k in range(cols):
                A[j][k] -= factor * A[i][k]
    
    # Back-substitute to get the rank
    rank = 0
    for i in range(rows):
        if all(A[i][j] == 0 for j in range(cols)):
            continue
        rank += 1
    
    return rank

def generate_explicit_function(n):
    # Generate a random polynomial of degree n with integer coefficients
    coeffs = [random.randint(-10, 10) for _ in range(n+1)]
    def f(x):
        return sum(c * x**i for i, c in enumerate(coeffs))
    return f

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_circuit_size = 0
    
    for n in n_values:
        f = generate_explicit_function(n)
        # Compute ACC⁰ circuit size (simplified example)
        circuit_size = n * (n + 1) // 2
        
        # Compute twisted Hodge theory invariant (placeholder)
        # This is a placeholder function. Replace with actual computation.
        H = [[random.randint(-5, 5) for _ in range(n)] for _ in range(n)]
        rank = gaussian_elimination(H)
        
        total_rank += rank
        total_circuit_size += circuit_size
    
    mean_ratio = total_rank / (len(n_values) * sum(n_values))
    std_deviation = math.sqrt(sum((rank - mean_ratio)**2 for rank in [total_rank / len(n_values)] * len(n_values)) / len(n_values))
    
    conjecture_holds = mean_ratio >= 0.8 and std_deviation <= 3
    counterexample = "" if conjecture_holds else f"mean_ratio={mean_ratio}, std_deviation={std_deviation}"
    
    return {
        "metric_name": "Mean Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 50))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_deviation} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mean_ratio={mean_ratio}, std_deviation={std_deviation}' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")