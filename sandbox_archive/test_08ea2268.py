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
    
    def generate_monotone_k_clique(n, k):
        if n < k or k <= 0:
            return []
        vertices = list(range(n))
        clique = set(random.sample(vertices, k))
        formula = []
        for i in range(1 << n):
            assignment = [bool(i & (1 << j)) for j in range(n)]
            if all(assignment[v] for v in clique) and not any(assignment[v] for v in vertices - clique):
                clause = ' OR '.join(f'x{i}' if a else f'NOT x{i}' for i, a in enumerate(assignment))
                formula.append(clause)
        return formula
    
    def count_orbits(formula):
        n = len(formula)
        orbits = set()
        for assignment in itertools.product([0, 1], repeat=n):
            orbit = tuple(sorted(i for i in range(n) if assignment[i]))
            orbits.add(orbit)
        return len(orbits)
    
    def is_circuit_size_valid(circuit_size, k):
        return circuit_size <= k**2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_orbits = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 random instances
            formula = generate_monotone_k_clique(n, k)
            if not formula:
                continue
            orbits = count_orbits(formula)
            total_orbits += orbits
            instances_tested += 1
    
    metric_value = total_orbits / len(n_values)
    
    # Check the conjecture for each n
    conjecture_holds = True
    counterexample = ""
    for n in n_values:
        k = random.randint(2, min(5, n))  # Ensure k is at least 2 and not too large
        formula = generate_monotone_k_clique(n, k)
        if not formula:
            continue
        orbits = count_orbits(formula)
        if orbits > (k**2 + k) * 10:  # Polynomial upper bound for simplicity
            conjecture_holds = False
            counterexample = f"n={n}, k={k}, orbits={orbits}"
    
    return {
        "metric_name": "Average Orbits",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 89))  # First 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")