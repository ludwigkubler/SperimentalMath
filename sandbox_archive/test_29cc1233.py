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
    
    def generate_tseitin_tree(n):
        if n == 1:
            return ['A']
        else:
            left = generate_tseitin_tree(n // 2)
            right = generate_tseitin_tree((n + 1) // 2)
            return [f'NOT {left[0]}', f'OR {right[0]} {left[1]}']
    
    def compute_hodge_rank(tree):
        if isinstance(tree, str):
            return 1
        else:
            left_rank = compute_hodge_rank(tree[1])
            right_rank = compute_hodge_rank(tree[2])
            return max(left_rank, right_rank) + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        tree = generate_tseitin_tree(n)
        rank = compute_hodge_rank(tree)
        expected_rank = math.log2(n)
        results.append({
            "n": n,
            "rank": rank,
            "expected_rank": expected_rank
        })
    
    total_instances_tested = len(results)
    mean_diff = sum(abs(r["rank"] - r["expected_rank"]) for r in results) / total_instances_tested
    conjecture_holds = all(math.isclose(r["rank"], r["expected_rank"], abs_tol=0.5) for r in results)
    
    return {
        "metric_name": "Hodge Rank",
        "metric_value": mean_diff,
        "instances_tested": total_instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "n={n}, rank={rank}, expected_rank={expected_rank}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={result['counterexample']}\", first_failing_seed={first_failing_seed}")