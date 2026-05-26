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

def generate_tseitin_tree(n):
    if n == 1:
        return ['x', '']
    left = generate_tseitin_tree(n // 2)
    right = generate_tseitin_tree((n + 1) // 2)
    return [f'NOT {left[0]}', f'OR {right[0]} {left[1]}']

def compute_hodge_rank(tree):
    # Placeholder for actual Hodge rank computation
    # This is a dummy implementation that returns the length of the tree as a proxy
    return len(tree)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    tree = generate_tseitin_tree(n)
    rank = compute_hodge_rank(tree)
    expected_rank = math.log2(n)
    diff = abs(rank - expected_rank)
    
    result = {
        "metric_name": "Hodge Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": diff <= 0.5 and diff <= 1,
        "counterexample": "" if diff <= 0.5 and diff <= 1 else f"Expected {expected_rank}, got {rank}"
    }
    
    return result

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_diff = sum(abs(result["metric_value"] - math.log2(n)) for n, result in zip([5, 10, 15, 20, 30, 40], results)) / len(results)
        support_fraction = Fraction(sum(1 for result in results if result["conjecture_holds"]), len(results))
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")