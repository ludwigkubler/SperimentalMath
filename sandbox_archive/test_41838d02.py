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
    
    def generate_frege_tree(depth):
        if depth == 0:
            return ['A']
        else:
            left = generate_frege_tree(random.randint(0, depth-1))
            right = generate_frege_tree(random.randint(0, depth-1))
            return [f'({left[0]} {right[0]})']
    
    def compute_min_rank(tree):
        if isinstance(tree, str):
            return 1
        else:
            left_rank = compute_min_rank(tree[1])
            right_rank = compute_min_rank(tree[2])
            return max(left_rank, right_rank) + 1
    
    n = random.randint(5, 40)
    depth = int(math.log(n))
    tree = generate_frege_tree(depth)
    
    min_rank = compute_min_rank(tree)
    conjecture_holds = min_rank <= depth and 2**depth >= depth
    counterexample = "" if conjecture_holds else f"min_rank={min_rank}, depth={depth}"
    
    return {
        "metric_name": "MinRank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")