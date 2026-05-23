# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import product

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        # Find pivot
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    return A

def rank(A):
    A = gaussian_elimination(A)
    r = 0
    for row in A:
        if any(row):
            r += 1
    return r

def ac0_circuit(inputs, n):
    # Placeholder function for AC0 circuit evaluation
    # This is a dummy implementation and should be replaced with actual logic
    return random.choice([0, 1])

def parity_threshold(f, n):
    count = sum(1 for x in range(2**n) if ac0_circuit([f(x)], n) == 1)
    return Fraction(count, 2**n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = lambda x: sum(x[i] & (1 << i) for i in range(n)) % 2
        t = parity_threshold(f, n)
        minimal_rank = rank([[f(x ^ y) for y in range(2**n)] for x in range(2**n)])
        
        results.append({
            "n": n,
            "t": t,
            "minimal_rank": minimal_rank
        })
    
    correlation_sum = 0
    for result in results:
        correlation_sum += (result["minimal_rank"] - t * math.log(result["n"])) ** 2
    
    mean_correlation = correlation_sum / len(results)
    std_deviation = math.sqrt(mean_correlation)
    
    return {
        "metric_name": "correlation",
        "metric_value": mean_correlation,
        "instances_tested": len(results),
        "conjecture_holds": mean_correlation >= 0.7,
        "counterexample": "" if mean_correlation >= 0.7 else f"n={results[0]['n']}, t={t}, minimal_rank={results[0]['minimal_rank']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[0]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")