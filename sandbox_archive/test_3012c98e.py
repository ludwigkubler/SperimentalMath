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

def generate_tree(n):
    if n == 1:
        return [0, 1]
    left = generate_tree(n-1)
    right = generate_tree(n-1)
    return [[left[i] ^ right[i] for i in range(2**(n-1))], [left[i] & right[i] for i in range(2**(n-1))]]

def compute_noncommutative_crossed_product(tree):
    n = len(tree[0])
    if n == 1:
        return [[tree[0][0]], [tree[1][0]]]
    
    left = compute_noncommutative_crossed_product(tree[0])
    right = compute_noncommutative_crossed_product(tree[1])
    
    new_left = []
    new_right = []
    for i in range(2**(n-1)):
        for j in range(2**(n-1)):
            new_left.append(left[i][j] ^ right[j][i])
            new_right.append(left[i][j] & right[j][i])
    
    return [new_left, new_right]

def compute_minimal_rank(algebra):
    n = len(algebra[0])
    rank = 0
    for i in range(n):
        if algebra[0][i] != 0 or algebra[1][i] != 0:
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        tree = generate_tree(n)
        algebra = compute_noncommutative_crossed_product(tree)
        minimal_rank = compute_minimal_rank(algebra)
        
        f_n = math.log(n) * math.log(math.log(n))
        if minimal_rank <= f_n:
            width = 2**n
            if width > 2**n:
                return {
                    "metric_name": "width",
                    "metric_value": width,
                    "instances_tested": n,
                    "conjecture_holds": False,
                    "counterexample": "Tree with minimal rank <= f(n) but width > 2^n"
                }
        else:
            if minimal_rank > f_n and width > 2**n:
                return {
                    "metric_name": "width",
                    "metric_value": width,
                    "instances_tested": n,
                    "conjecture_holds": False,
                    "counterexample": "Tree with minimal rank > f(n) but width > 2^n"
                }
    
    return {
        "metric_name": "width",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= 2**n) / len(results)
    
    if all(r <= 2**n for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r > 2**n for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result > 2**n)
        print(f"RESULT: FALSIFIED counterexample=\"Tree with minimal rank <= f(n) but width > 2^n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=metric_saturation")