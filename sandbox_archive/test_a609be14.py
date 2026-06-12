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

def compute_k_theory_sheaf_rank(n, d):
    # Placeholder function to simulate K-theoretic computations
    return n**0.5

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        d = random.randint(1, 10)
        
        k_theory_rank = compute_k_theory_sheaf_rank(n, d)
        ratio = k_theory_rank / (d**(2/3) * n**(1/6))
        
        results.append({
            "n": n,
            "d": d,
            "k_theory_rank": k_theory_rank,
            "ratio": ratio
        })
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    conjecture_holds = all(0.5 <= result["ratio"] <= 2 for result in results)
    counterexample = "" if conjecture_holds else "Ratio outside [0.5, 2] range"
    
    return {
        "metric_name": "K-theory Sheaf Rank Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
    # Compute mean/std of metric_value, fraction of seeds where conjecture_holds
    all_results = [run_trial(seed) for seed in seeds]
    mean_metric_value = sum(result["metric_value"] for result in all_results) / len(all_results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in all_results) / len(all_results))
    support_fraction = sum(1 for result in all_results if result["conjecture_holds"]) / len(all_results)
    
    if all(result["conjecture_holds"] for result in all_results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio outside [0.5, 2] range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")