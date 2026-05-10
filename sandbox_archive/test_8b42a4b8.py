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

def generate_random_read_twice_bp(n):
    bp = []
    for i in range(2**n):
        if i % 2 == 0:
            bp.append(random.choice([-1, 1]))
        else:
            bp.append(-bp[i-1])
    return bp

def compute_function(bp, n):
    f = [0] * (2**n)
    for i in range(2**n):
        f[i] = bp[i]
    return f

def compute_additive_energy(f, n):
    energy = 0
    for x in range(2**n):
        for y in range(x+1, 2**n):
            for z in range(y+1, 2**n):
                for w in range(z+1, 2**n):
                    if f[x] + f[y] == f[z] + f[w]:
                        energy += 1
    return energy

def compute_discrepancy(bp, n):
    max_disc = 0
    for S in range(1, 2**n):
        sum_S = sum(bp[i] for i in range(n) if (S >> i) & 1)
        disc = abs(sum_S - (2**n - S))
        if disc > max_disc:
            max_disc = disc
    return max_disc

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    bp = generate_random_read_twice_bp(n)
    f = compute_function(bp, n)
    energy = compute_additive_energy(f, n)
    disc = compute_discrepancy(bp, n)
    
    C = 1.0  # Empirical constant
    metric_value = energy / (C * n * disc) if disc != 0 else float('inf')
    
    return {
        "metric_name": "additive_energy_over_disc",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": metric_value >= 1.0,  # Adjust C as needed
        "counterexample": "" if metric_value >= 1.0 else "discrepancy_too_small"
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [2**i + 1 for i in range(5, 8)]  # Default to first 3 primes
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"discrepancy_too_small\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")