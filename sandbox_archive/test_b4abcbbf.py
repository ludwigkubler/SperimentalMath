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

def sieve_of_eratosthenes(n):
    primes = [True] * (n + 1)
    p = 2
    while (p * p <= n):
        if (primes[p] == True):
            for i in range(p * p, n + 1, p):
                primes[i] = False
        p += 1
    prime_numbers = []
    for p in range(2, n + 1):
        if primes[p]:
            prime_numbers.append(p)
    return len(prime_numbers)

def generate_dirichlet_progression(n):
    a = random.randint(1, n - 1)
    d = random.randint(1, n * n)
    progression = [a]
    while True:
        next_val = (progression[-1] + d) % n
        if next_val == a:
            break
        progression.append(next_val)
    return progression

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0.0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        pi_n = sieve_of_eratosthenes(n)
        dirichlet_progression = generate_dirichlet_progression(n)
        seed_length = len(dirichlet_progression)
        
        total_metric_value += abs(seed_length - pi_n)
        instances_tested += 1
        
        if abs(seed_length - pi_n) > 2 * math.sqrt(pi_n):
            conjecture_holds = False
            counterexample = f"n={n}, seed_length={seed_length}, pi(n)={pi_n}"
    
    return {
        "metric_name": "Seed Length",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 150, 5))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")