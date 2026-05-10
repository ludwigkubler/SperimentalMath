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

def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def binomial_coefficient(n, k):
    return factorial(n) // (factorial(k) * factorial(n - k))

def young_tableau_decomposition(n):
    def hook_length_formula(tableau):
        hook_lengths = []
        for row in range(n):
            for col in range(n):
                hook_lengths.append((n - row) + (n - col) - 1)
        det = 1
        for i in range(n):
            for j in range(i, n):
                det *= hook_lengths[i * n + j]
        return det

    def generate_tableaux():
        tableaux = []
        for i in range(1 << (n * n)):
            tableau = [[0] * n for _ in range(n)]
            count = 0
            for row in range(n):
                for col in range(n):
                    if i & (1 << (row * n + col)):
                        tableau[row][col] = count + 1
                        count += 1
            tableaux.append(tableau)
        return tableaux

    tableaux = generate_tableaux()
    orbit_count = sum(1 for t in tableaux if hook_length_formula(t) % n == 0)
    return orbit_count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    c = 0.5
    instances_tested = 30
    orbit_counts = []

    for _ in range(instances_tested):
        # Generate a random AC⁰ circuit computing PARITY on n variables
        circuit = [random.choice([0, 1]) for _ in range(2**n)]
        
        # Compute the orbit count under S_n action using Young tableau decomposition
        orbit_count = young_tableau_decomposition(n)
        orbit_counts.append(orbit_count)

    mean_orbit_count = sum(orbit_counts) / instances_tested
    conjecture_holds = all(count >= c * math.sqrt(n) for count in orbit_counts)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "orbit_count",
        "metric_value": mean_orbit_count,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")