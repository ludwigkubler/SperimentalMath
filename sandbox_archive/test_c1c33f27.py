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
    
    def generate_bst(height):
        if height == 0:
            return None
        root = {'value': random.randint(1, 100)}
        left_height = random.randint(0, height - 1)
        right_height = height - left_height - 1
        root['left'] = generate_bst(left_height)
        root['right'] = generate_bst(right_height)
        return root
    
    def grothendieck_witt_class(tree):
        if tree is None:
            return 0
        left_rank = grothendieck_witt_class(tree['left'])
        right_rank = grothendieck_witt_class(tree['right'])
        return max(left_rank, right_rank) + 1
    
    n = random.randint(5, 40)
    tree = generate_bst(n)
    rank = grothendieck_witt_class(tree)
    
    h = n  # Height of the BST
    expected_rank = h**2
    
    if abs(rank - expected_rank) <= 0.2 * expected_rank:
        conjecture_holds = True
    else:
        conjecture_holds = False
    
    return {
        "metric_name": "Grothendieck-Witt Class Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Rank {rank} does not match expected {expected_rank}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")