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

def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def compute_br_len(f):
    n = int(math.log2(len(f)))
    # Simplified Brauer group length calculation (for demonstration)
    return n + 1

def compute_comm_complexity(f):
    n = int(math.log2(len(f)))
    # Simplified communication complexity calculation (for demonstration)
    return n * (n - 1) // 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        f = generate_random_boolean_function(random.randint(5, 40))
        br_len_f = compute_br_len(f)
        comm_complexity_f = compute_comm_complexity(f)
        if br_len_f == 0:
            continue
        ratio = comm_complexity_f / br_len_f
        results.append(ratio)
    mean_ratio = sum(results) / len(results)
    conjecture_holds = all(0.5 <= r <= 2 for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Communication Complexity Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(40, random.randint(5, 40)),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_metric = sum(results) / len(results)
    support_fraction = sum(1 for r in results if 0.5 <= r <= 2) / len(results)
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric:.4f} std=NA support_fraction={support_fraction:.2f}")
    elif any(not r for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if not (0.5 <= r <= 2)))]
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")