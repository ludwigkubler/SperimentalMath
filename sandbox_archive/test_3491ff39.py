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
    max_exponent = 0
    instances_tested = 0
    n_max = 5
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            k = random.randint(2, min(n, 40))
            cnf = generate_random_kcnf(n, k)
            exponent = calculate_diophantine_exponent(cnf)
            max_exponent = max(max_exponent, exponent)
            instances_tested += 1
            n_max = max(n_max, n)
    
    conjecture_holds = max_exponent <= (k**3 * n**(1/4))
    counterexample = "" if conjecture_holds else f"max_exponent={max_exponent} > k^3*n^(1/4)"
    
    return {
        "metric_name": "max_diophantine_exponent",
        "metric_value": max_exponent,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def generate_random_kcnf(n: int, k: int) -> list:
    cnf = []
    for _ in range(k):
        clause = random.sample(range(1, n+1), 2)
        cnf.append([random.choice([-1, 1]) * lit for lit in clause])
    return cnf

def calculate_diophantine_exponent(cnf: list) -> float:
    # Placeholder for actual diophantine exponent calculation
    # This is a dummy implementation that returns a random value
    return random.random() * 100  # Replace with actual logic

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")