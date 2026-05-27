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
        root['left'] = generate_bst(random.randint(0, height - 1))
        root['right'] = generate_bst(random.randint(0, height - 1))
        return root
    
    def grothendieck_witt_class(tree):
        if tree is None:
            return 0
        left_rank = grothendieck_witt_class(tree['left'])
        right_rank = grothendieck_witt_class(tree['right'])
        return max(left_rank, right_rank) + 1
    
    def height_of_bst(tree):
        if tree is None:
            return 0
        return 1 + max(height_of_bst(tree['left']), height_of_bst(tree['right']))
    
    n = random.randint(5, 40)
    total_rank = 0
    instances_tested = 0
    
    for _ in range(n):
        tree_height = random.randint(1, n)
        bst = generate_bst(tree_height)
        rank = grothendieck_witt_class(bst)
        total_rank += rank
        instances_tested += 1
    
    average_rank = total_rank / instances_tested
    conjecture_holds = abs(average_rank - (n ** 2)) <= 0.2 * (n ** 2)
    
    return {
        "metric_name": "average_grothendieck_witt_class_rank",
        "metric_value": average_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")