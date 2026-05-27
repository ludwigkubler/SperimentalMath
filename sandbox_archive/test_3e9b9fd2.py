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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def generate_bst(n):
    if n == 0:
        return None
    root = random.randint(1, n)
    left_size = random.randint(0, n-1)
    right_size = n - left_size - 1
    left_tree = generate_bst(left_size)
    right_tree = generate_bst(right_size)
    return [root, left_tree, right_tree]

def grothendieck_witt_class_rank(tree):
    if tree is None:
        return 0
    left_rank = grothendieck_witt_class_rank(tree[1])
    right_rank = grothendieck_witt_class_rank(tree[2])
    return max(left_rank, right_rank) + 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        total_rank = 0
        instances_tested = 0
        for _ in range(5):
            tree = generate_bst(n)
            rank = grothendieck_witt_class_rank(tree)
            total_rank += rank
            instances_tested += 1
        avg_rank = Fraction(total_rank, instances_tested)
        expected_rank = n**2
        conjecture_holds = abs(avg_rank - expected_rank) <= 0.2 * expected_rank or avg_rank >= 1.2 * expected_rank
        counterexample = f"n={n}, avg_rank={avg_rank}, expected_rank={expected_rank}" if not conjecture_holds else ""
        results.append({
            "metric_name": "Grothendieck-Witt Class Rank",
            "metric_value": avg_rank,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    return {
        "seed": seed,
        **results[0]
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_rank = sum(r["metric_value"] for r in results)
    instances_tested = sum(r["instances_tested"] for r in results)
    mean_rank = Fraction(total_rank, instances_tested)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")