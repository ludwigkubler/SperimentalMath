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

def generate_xor_and_tree(n):
    if n == 1:
        return ['x1']
    else:
        left = generate_xor_and_tree(n // 2)
        right = generate_xor_and_tree(n - n // 2)
        return [f'({left[0]} & {right[0]}) | ({left[1]} & {right[1]})']

def construct_quantum_group_representation(tree):
    if len(tree) == 1:
        return [tree[0]]
    else:
        left = construct_quantum_group_representation([tree[2]])
        right = construct_quantum_group_representation([tree[4]])
        return [f'({left[0]} & {right[0]}) | ({left[1]} & {right[1]})']

def communication_complexity(tree):
    if len(tree) == 1:
        return 1
    else:
        left = communication_complexity([tree[2]])
        right = communication_complexity([tree[4]])
        return max(left, right) + 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    tree = generate_xor_and_tree(n)
    generators = construct_quantum_group_representation(tree)
    
    rank = len(generators)
    width = communication_complexity(tree)
    
    if width == 0:
        return {
            "metric_name": "rank/width",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "tree_width_zero"
        }
    
    ratio = rank / width
    expected_ratio = math.log(n)
    
    return {
        "metric_name": "rank/width",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": abs(ratio - expected_ratio) <= expected_ratio * 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "rank/width_ratio_out_of_bounds"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")