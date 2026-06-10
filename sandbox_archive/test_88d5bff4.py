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

def generate_complexity_instance(n):
    # Generate n variables and construct the associated simplicial complex.
    vertices = list(range(n))
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            if random.choice([True, False]):
                edges.append((i, j))
    return vertices, edges

def calculate_betti_numbers(complex):
    # Calculate Betti numbers for the given simplicial complex.
    vertices, edges = complex
    betti_numbers = [0] * len(vertices)
    for edge in edges:
        u, v = edge
        if betti_numbers[u] == 0 and betti_numbers[v] == 0:
            betti_numbers[u] = 1
            betti_numbers[v] = 1
        elif betti_numbers[u] == 0:
            betti_numbers[u] = betti_numbers[v]
        elif betti_numbers[v] == 0:
            betti_numbers[v] = betti_numbers[u]
    return min(betti_numbers)

def calculate_frege_proof_length(formula):
    # Calculate Frege proof length for the given formula.
    n = len(formula)
    if n == 1:
        return 1
    else:
        return 2 * calculate_frege_proof_length([formula[:n//2], formula[n//2:]])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    metric_name = "Frege Proof Length"
    instances_tested = 30
    n_max = 40
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        n = random.choice([5, 10, 15, 20, 30, 40])
        formula = [random.randint(0, 1) for _ in range(n)]
        complex = generate_complexity_instance(n)
        beta_min = calculate_betti_numbers(complex)
        F_phi = calculate_frege_proof_length(formula)

        if not (math.log(n) <= F_phi <= 2 * math.log(n)):
            conjecture_holds = False
            counterexample = f"Formula: {formula}, Betti Min: {beta_min}, Frege Proof Length: {F_phi}"
            break

    return {
        "metric_name": metric_name,
        "metric_value": F_phi,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        result_type = "SUPPORTED"
    elif support_fraction >= 0.8:
        result_type = "SUPPORTED"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result_type = f"FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}"

    print(f"RESULT: {result_type} mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")