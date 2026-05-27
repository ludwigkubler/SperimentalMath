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
    
    def generate_xor_and_tree(w):
        if w == 1:
            return [0, 1]
        else:
            left = generate_xor_and_tree(w // 2)
            right = generate_xor_and_tree(w - w // 2)
            return [left, right]

    def compute_minimal_rank(tree):
        if isinstance(tree[0], list) and isinstance(tree[1], list):
            rank_left = compute_minimal_rank(tree[0])
            rank_right = compute_minimal_rank(tree[1])
            return max(rank_left, rank_right) + 1
        else:
            return 1

    def dpll_refutation_size(tree):
        if isinstance(tree[0], list) and isinstance(tree[1], list):
            size_left = dpll_refutation_size(tree[0])
            size_right = dpll_refutation_size(tree[1])
            return max(size_left, size_right) + 2
        else:
            return 1

    n_tests = 30
    total_rank = 0
    max_rank = 0
    
    for _ in range(n_tests):
        w = random.randint(5, 40)
        tree = generate_xor_and_tree(w)
        rank = compute_minimal_rank(tree)
        refutation_size = dpll_refutation_size(tree)
        
        total_rank += rank
        max_rank = max(max_rank, rank)
        
        if rank > 1.5 * w**2:
            return {
                "metric_name": "minimal_rank",
                "metric_value": rank,
                "instances_tested": n_tests,
                "conjecture_holds": False,
                "counterexample": f"Rank {rank} exceeds 1.5w^2 for width {w}"
            }
    
    mean_rank = total_rank / n_tests
    std_dev = math.sqrt(sum((x - mean_rank) ** 2 for x in range(n_tests)) / n_tests)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": n_tests,
        "conjecture_holds": 0.5 * w**2 <= mean_rank <= 1.5 * w**2 and std_dev < 0.1 * w**2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds 1.5w^2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")