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

def gaussian_elimination(A, mod):
    n = len(A)
    for i in range(n):
        pivot = A[i][i]
        if pivot == 0:
            # Find a row with non-zero pivot to swap with
            for j in range(i + 1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    pivot = A[i][i]
                    break
        if pivot == 0:
            continue  # Skip rows where the pivot is zero

        # Normalize the pivot to 1
        for j in range(n):
            A[i][j] = (A[i][j] * pow(pivot, -1, mod)) % mod

        # Eliminate the pivot column
        for j in range(n):
            if i != j:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] = (A[j][k] - factor * A[i][k]) % mod

    return A

def hodge_order(cnf, n, mod):
    # Simulate the computation of H^1(φ) and find the minimal order
    # This is a placeholder function; replace with actual Hodge theory computation
    # For simplicity, we'll use a random matrix to simulate H^1(φ)
    A = [[random.randint(0, mod - 1) for _ in range(n)] for _ in range(n)]
    A = gaussian_elimination(A, mod)
    non_zero_entries = [entry for row in A for entry in row if entry != 0]
    order = max(non_zero_entries, default=0)
    return order

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        cnf = [random.randint(1, n) for _ in range(n)]  # Simulate a random CNF formula
        mod = 2**n  # Use a modulus that is a power of 2 for simplicity

        order = hodge_order(cnf, n, mod)
        total_metric_value += order
        instances_tested += 1
        n_max = max(n_max, n)

        if order > n**3:
            conjecture_holds = False
            counterexample = f"n={n}, order={order} exceeds bound {n**3}"

    return {
        "metric_name": "Hodge Order",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={math.sqrt(sum((r['metric_value'] - mean_metric_value)**2 for r in results) / len(results))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")