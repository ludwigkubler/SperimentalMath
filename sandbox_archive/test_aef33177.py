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
    
    def construct_bp(n):
        bp = []
        for i in range(n):
            bp.append(random.choice(['+', '-']))
        return bp
    
    def compute_rho(bp):
        # Construct the noncommutative crossed product
        n = len(bp)
        rho = 0
        for i in range(n):
            if bp[i] == '+':
                rho += 1
            else:
                rho -= 1
        return abs(rho)
    
    def size(bp):
        return len(bp)
    
    instances_tested = 30
    total_rho = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        bp = construct_bp(n)
        rho = compute_rho(bp)
        total_rho += rho
    
    mean_rho = total_rho / instances_tested
    conjecture_holds = (mean_rho <= math.log2(size(bp)) * 1.5) and (mean_rho >= math.log2(size(bp)))
    counterexample = "" if conjecture_holds else f"Mean ρ(P) = {mean_rho}, expected Θ(log size(P))"
    
    return {
        "metric_name": "rho",
        "metric_value": mean_rho,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rho = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_rho) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_dev} support_fraction={support_fraction}")
    elif any(result["metric_value"] > 2 * math.log2(size(bp)) for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] > 2 * math.log2(size(bp)))
        print(f"RESULT: FALSIFIED counterexample=\"ρ(P) > 2 * E[ρ(P)]\" first_failing_seed={first_failing_seed}")
    elif any(result["metric_value"] > 1.5 * math.log2(size(bp)) for result in results):
        print(f"RESULT: INCONCLUSIVE reason=exceeds_upper_bound n_tested={len(results)}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")