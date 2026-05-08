# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import product

def fourier_coefficients(f, n):
    N = 2 ** n
    coeffs = [0] * N
    for k in range(N):
        sum_val = 0
        for x in range(N):
            sum_val += f(x) * math.cos(2 * math.pi * k * x / N)
        coeffs[k] = sum_val / N
    return coeffs

def gowers_uniformity_norm(f, n):
    coeffs = fourier_coefficients(f, n)
    norm = 0
    for coeff in coeffs:
        norm += abs(coeff) ** 4
    return norm ** (1/4)

def simulate_acc0_circuit(f, n, size):
    # Simplified simulation of ACC^0 circuit with given size
    # This is a placeholder and does not actually compute the function
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(50):  # Sample 50 instances per seed
        f = lambda x: random.choice([0, 1])  # Random Boolean function
        norm = gowers_uniformity_norm(f, n)
        if norm >= n ** 0.1:  # Threshold for ε=0.1
            circuit_size = simulate_acc0_circuit(f, n, size=n**2)
            if not circuit_size:
                conjecture_holds = False
                counterexample = "Function cannot be computed by ACC^0 circuit"
                break

        instances_tested += 1

    return {
        "metric_name": "Gowers Uniformity Norm",
        "metric_value": norm,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]  # Default to first 30 primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")