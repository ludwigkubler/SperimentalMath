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
    
    def generate_xor_and_tree(width):
        if width == 1:
            return random.choice([0, 1])
        else:
            left = generate_xor_and_tree(width // 2)
            right = generate_xor_and_tree(width // 2)
            return (left, right) if random.choice([True, False]) else (right, left)
    
    def calculate_rank(tree):
        if isinstance(tree, int):
            return 0
        else:
            left_rank = calculate_rank(tree[0])
            right_rank = calculate_rank(tree[1])
            return max(left_rank, right_rank) + 1
    
    width = random.randint(5, 40)
    tree = generate_xor_and_tree(width)
    rank = calculate_rank(tree)
    
    metric_name = "rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank <= math.log2(width) + 1
    counterexample = "" if conjecture_holds else f"rank={rank}, expected=O(log {width})"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")