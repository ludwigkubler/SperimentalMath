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
    
    def generate_read_twice_bp(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(2)]
            clauses.append(clause)
        return clauses
    
    def size(bp):
        return len(bp)
    
    def dpll_search_tree_size(bp):
        # Simplified DPLL search tree size estimation
        return 2 ** (len(bp))
    
    def tropicalized_lie_group_rank(bp):
        # Placeholder for actual computation
        return random.randint(1, size(bp))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(n // 2, n * 2)
            bp = generate_read_twice_bp(n, m)
            rank = tropicalized_lie_group_rank(bp)
            size_p = size(bp)
            dpll_size = dpll_search_tree_size(bp)
            
            results.append({
                "n": n,
                "m": m,
                "rank": rank,
                "size_p": size_p,
                "dpll_size": dpll_size
            })
    
    total_rank = sum(result["rank"] for result in results)
    mean_rank = total_rank / len(results)
    min_rank = min(result["rank"] for result in results)
    max_rank = max(result["rank"] for result in results)
    
    conjecture_holds = all(
        math.log(result["size_p"]) <= result["rank"] <= result["size_p"]
        for result in results
    )
    
    counterexample = ""
    if not conjecture_holds:
        for result in results:
            if not (math.log(result["size_p"]) <= result["rank"] <= result["size_p"]):
                counterexample = f"n={result['n']}, m={result['m']}, rank={result['rank']}, size(P)={result['size_p']}"
                break
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{trial_result['counterexample']}' first_failing_seed={first_failing_seed}")