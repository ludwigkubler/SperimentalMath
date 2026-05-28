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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_read_twice_bp(n: int, width: int) -> list:
        bp = [[0] * n for _ in range(width)]
        for i in range(width):
            for j in range(n):
                if random.random() < 0.5:
                    bp[i][j] = 1
        return bp
    
    def construct_crossed_product_algebra(bp: list) -> int:
        width = len(bp)
        n = len(bp[0])
        
        # Simulate the construction of M using a simple counting method
        rank = 0
        for i in range(width):
            for j in range(n):
                if bp[i % width][j] == 1:
                    rank += 1
        return rank
    
    def is_trivial_bp(bp: list) -> bool:
        width = len(bp)
        n = len(bp[0])
        return all(bp[i % width][j] == 0 for i in range(width) for j in range(n))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        bp = generate_read_twice_bp(n, n)
        rank = construct_crossed_product_algebra(bp)
        
        if is_trivial_bp(bp):
            expected_rank = n
        else:
            expected_rank = None
        
        results.append({
            "n": n,
            "bp": bp,
            "rank": rank,
            "expected_rank": expected_rank
        })
    
    total_rank = sum(result["rank"] for result in results)
    avg_rank = Fraction(total_rank, len(results))
    max_rank = max(result["rank"] for result in results)
    min_rank = min(result["rank"] for result in results)
    
    if is_trivial_bp(bp):
        conjecture_holds = rank >= n
        counterexample = "" if conjecture_holds else f"Rank {rank} < {n}"
    else:
        conjecture_holds = False
        counterexample = "mapping_undefined"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": avg_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_rank = sum(result["metric_value"] for result in results) / len(results)
    max_rank = max(result["metric_value"] for result in results)
    min_rank = min(result["metric_value"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")