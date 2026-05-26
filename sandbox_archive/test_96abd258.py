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
    
    def generate_and_or_tree(depth, leaves):
        if depth == 0:
            return random.choice(leaves)
        else:
            left = generate_and_or_tree(depth - 1, leaves)
            right = generate_and_or_tree(depth - 1, leaves)
            return (left, right)

    def compute_min_rank(tree, leaves):
        if isinstance(tree, tuple):
            left, right = tree
            rank_left = compute_min_rank(left, leaves)
            rank_right = compute_min_rank(right, leaves)
            return max(rank_left, rank_right) + 1
        else:
            return 1

    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    if not all(is_prime(int(s)) for s in sys.argv[1:]):
        return {
            "metric_name": "minRank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        D = random.randint(1, min(n, 40))
        tree = generate_and_or_tree(D, list(range(n)))
        rank = compute_min_rank(tree, list(range(n)))
        results.append(rank)
    
    mean_rank = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_rank) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r - (n**2)) < n**2 // 4) / len(results)
    
    return {
        "metric_name": "minRank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"mean={mean_rank}, std={std_dev}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean={mean_rank}, std={std_dev}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")