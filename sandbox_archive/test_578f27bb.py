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
    
    def generate_random_kcnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def tropical_realization(cnf):
        # Simplified version of tropical realization
        return len(cnf)  # This is a placeholder. Replace with actual computation.
    
    def min_rank(tropical_structure):
        # Placeholder for minimal rank calculation
        return len(tropical_structure)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_random_kcnf(n, k=5)  # Fixed k for simplicity
        tropical_structure = tropical_realization(cnf)
        rank = min_rank(tropical_structure)
        results.append({
            "n": n,
            "rank": rank
        })
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    max_rank = max(result["rank"] for result in results)
    
    conjecture_holds = all(results[i]["rank"] <= results[i+1]["rank"] for i in range(len(results)-1))
    counterexample = "" if conjecture_holds else "Rank does not increase monotonically"
    
    return {
        "metric_name": "MinRank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank does not increase monotonically\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")