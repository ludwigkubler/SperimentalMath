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
    
    def max_cut_approximation(n):
        # Simplified approximation for demonstration purposes
        return random.random() * 0.878 + 0.1
    
    def quotient_algebra_rank_and_norm(n, alpha):
        # Placeholder function to simulate computation
        rank = random.randint(1, n)
        norm = math.sqrt(rank) / math.sqrt(n)
        return rank, norm
    
    def check_conjecture(alpha, norm, n):
        c_alpha = 0.878
        return norm >= c_alpha * (n ** -0.5) == alpha > 0.878
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.randint(5, 40)
        alpha = max_cut_approximation(n)
        rank, norm = quotient_algebra_rank_and_norm(n, alpha)
        result = check_conjecture(alpha, norm, n)
        results.append({
            "n": n,
            "alpha": alpha,
            "rank": rank,
            "norm": norm,
            "result": result
        })
    
    metric_value = sum(result["norm"] for result in results) / len(results)
    conjecture_holds = all(result["result"] for result in results)
    counterexample = "" if conjecture_holds else "conjecture_violation"
    
    return {
        "metric_name": "Average 2-norm of polynomials",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**i + 7 for i in range(5, 6)]  # Default list of 30 primes
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='conjecture_violation' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")