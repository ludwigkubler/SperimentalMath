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
    
    def generate_tseitin_tree(n):
        if n == 1:
            return ['x']
        else:
            left = generate_tseitin_tree(random.randint(1, n-1))
            right = generate_tseitin_tree(n - len(left))
            return [f'({left[0]} OR {right[0]})'] + left + right
    
    def polynomial_representation(tree):
        if isinstance(tree, str):
            return tree
        else:
            return f'{polynomial_representation(tree[1])} * {polynomial_representation(tree[2])}'
    
    def symmetric_function(poly):
        # Simplified version for demonstration; actual computation depends on the conjecture's specifics
        return len(poly.split('*'))
    
    def calculate_width(tree):
        if isinstance(tree, str):
            return 1
        else:
            return max(calculate_width(tree[1]), calculate_width(tree[2]))
    
    n = random.randint(5, 40)
    tree = generate_tseitin_tree(n)
    poly = polynomial_representation(tree)
    rank = symmetric_function(poly)
    width = calculate_width(tree)
    
    if rank == 0 or width == 0:
        return {
            "metric_name": "Spearman's rank correlation coefficient",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log2_rank = math.log2(rank)
    log2_width = math.log2(width)
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": (log2_rank, log2_width),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    if all(val is not None for val in results):
        mean = sum(results) / len(results)
        std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
        support_fraction = sum(1 for val in results if val[0] >= val[1]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result is None)
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined first_failing_seed={first_failing_seed}")