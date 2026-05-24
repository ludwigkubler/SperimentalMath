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

def generate_and_or_tree(n):
    if n == 1:
        return 'A'
    else:
        left = generate_and_or_tree(random.randint(1, n-1))
        right = generate_and_or_tree(n - len(left) - 1)
        return ('O', left, right)

def compute_coxeter_number(root):
    if root == 'A':
        return 1
    elif isinstance(root, tuple):
        left, _, _ = root
        return max(compute_coxeter_number(left), compute_coxeter_number(right)) + 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            tree = generate_and_or_tree(n)
            coxeter_number = compute_coxeter_number(tree)
            root_system_length = math.log(coxeter_number, 2) if coxeter_number > 0 else float('inf')
            
            if root_system_length < 0 or not isinstance(root_system_length, (int, float)):
                conjecture_holds = False
                counterexample = "Invalid root system length"
                break
            
            depth = compute_tree_depth(tree)
            if depth > n:
                conjecture_holds = False
                counterexample = f"Tree depth {depth} exceeds log(n)={n}"
                break
            
            total_metric_value += root_system_length / math.log(n, 2)
            instances_tested += 1

    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else float('nan')
    support_fraction = instances_tested / (len(n_values) * 5)

    return {
        "metric_name": "Root System Length",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def compute_tree_depth(tree):
    if isinstance(tree, tuple):
        left, _, _ = tree
        return 1 + max(compute_tree_depth(left), compute_tree_depth(right))
    else:
        return 0

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 53))  # First 30 primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if not math.isnan(r["metric_value"])) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(math.isclose(r["metric_value"], mean_metric_value, rel_tol=0.5) for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=nan support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Depth exceeds log(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")