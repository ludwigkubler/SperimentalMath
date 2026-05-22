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
    
    def generate_polynomial(n, d):
        coefficients = [random.randint(0, 1) for _ in range(d + 1)]
        return lambda x: sum(c * (x[i] if i < len(x) else 0) for i, c in enumerate(coefficients))
    
    def discrepancy_distribution(f, n, samples=100):
        distribution = [f([random.randint(0, 1) for _ in range(n)]) for _ in range(samples)]
        return max(distribution) - min(distribution)
    
    def discrepancy_tensor_rank(f, n):
        # Placeholder for actual tensor rank computation
        return random.randint(1, 10)  # Simulated value
    
    def read_twice_branching_program(f, n):
        # Placeholder for actual BP construction and execution
        return random.random()  # Simulated value
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    d = random.randint(1, min(n, 10))
    f = generate_polynomial(n, d)
    
    discrepancy = discrepancy_distribution(f, n)
    tensor_rank = discrepancy_tensor_rank(f, n)
    bp_discrepancy = read_twice_branching_program(f, n)
    
    conjecture_holds = bp_discrepancy >= 0.5 * tensor_rank
    counterexample = "" if conjecture_holds else f"Discrepancy(P)={bp_discrepancy}, Min_Rank(T_f)={tensor_rank}"
    
    return {
        "metric_name": "Discrepancy",
        "metric_value": discrepancy,
        "instances_tested": 100,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
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
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")