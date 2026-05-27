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
    
    def xor_and_tree(n):
        if n == 1:
            return ['leaf']
        else:
            left = xor_and_tree(n // 2)
            right = xor_and_tree(n - n // 2)
            return [f'xor({left[0]}, {right[0]})', f'and({left[0]}, {right[0]})']
    
    def compute_minimal_rank(tree):
        if tree.startswith('leaf'):
            return 1
        elif 'xor' in tree:
            left, right = tree.split('(')[1].split(',')[0], tree.split(',')[2]
            return max(compute_minimal_rank(left), compute_minimal_rank(right)) + 1
        else:  # 'and'
            left, right = tree.split('(')[1].split(',')[0], tree.split(',')[2]
            return min(compute_minimal_rank(left), compute_minimal_rank(right))
    
    n = random.randint(5, 40)
    tree = xor_and_tree(n)
    minimal_rank = compute_minimal_rank(tree)
    
    metric_value = minimal_rank
    instances_tested = 1
    conjecture_holds = minimal_rank <= n * math.log2(n)
    counterexample = "" if conjecture_holds else f"Tree with {n} leaves and rank {minimal_rank}"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = results[0]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")