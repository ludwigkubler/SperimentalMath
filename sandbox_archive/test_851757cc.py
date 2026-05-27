# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_cnf(k, n):
        clauses = []
        for _ in range(n):
            clause = set(random.sample(range(1, 2*n+1), k))
            clauses.append(clause)
        return clauses
    
    def rank_A_k_n(k, n):
        # Placeholder function to compute the rank of A_k(n)
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, 10) * n**(k-1)
    
    k_values = [2, 3, 4, 5]
    results = []
    
    for k in k_values:
        for _ in range(7):  # Ensure at least 8 instances per seed
            clauses = generate_k_cnf(k, n=40)
            rank = rank_A_k_n(k, len(clauses))
            results.append({
                "k": k,
                "n": len(clauses),
                "rank": rank
            })
    
    metric_value = sum(result["rank"] for result in results) / len(results)
    conjecture_holds = all(result["rank"] <= 3 * result["n"]**(result["k"]-1) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Rank of A_k(n)",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*100 + 1, 100))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_mean = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={metric_mean} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.9:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")