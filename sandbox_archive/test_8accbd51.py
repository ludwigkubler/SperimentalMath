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
    
    def generate_xor_and_tree(n):
        if n == 1:
            return ['A']
        else:
            left = generate_xor_and_tree(n // 2)
            right = generate_xor_and_tree((n + 1) // 2)
            return [f'({left[0]} {right[0]})'] + left + right
    
    def tree_width(tree):
        if isinstance(tree, str):
            return 1
        else:
            return max(tree_width(child) for child in tree[1:]) + 1
    
    def quandle_structure_size(tree):
        if isinstance(tree, str):
            return 1
        else:
            left_size = quandle_structure_size(tree[1])
            right_size = quandle_structure_size(tree[2])
            return max(left_size, right_size) + 1
    
    n = random.randint(5, 40)
    tree = generate_xor_and_tree(n)
    tw = tree_width(tree)
    r_quandle = quandle_structure_size(tree)
    
    if r_quandle > 10 * tw:  # Example constant c=10
        return {
            "metric_name": "minimal_rank",
            "metric_value": r_quandle,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"r_quandle={r_quandle}, expected<=10*{tw}"
        }
    else:
        return {
            "metric_name": "minimal_rank",
            "metric_value": r_quandle,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)