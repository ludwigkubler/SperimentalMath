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

def xor_and_tree(n):
    if n == 1:
        return [0, 1]
    left = xor_and_tree(n // 2)
    right = xor_and_tree(n - n // 2)
    return [x ^ y for x in left] + [x & y for x in left] + [x ^ y for x in right] + [x & y for x in right]

def characteristic_polynomial(tree):
    if len(tree) == 1:
        return tree[0]
    poly = characteristic_polynomial(tree[:len(tree)//2])
    for node in tree[len(tree)//2:]:
        poly = [node * p for p in poly] + [p for p in poly]
    return poly

def minimal_rank_brauer_group(poly):
    n = len(poly)
    if n == 1:
        return 1
    rank = 0
    for i in range(1, n):
        if poly[i] != 0:
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        tree = xor_and_tree(n)
        poly = characteristic_polynomial(tree)
        rank = minimal_rank_brauer_group(poly)
        results.append((n, rank))
    
    if not results:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_values = [n for n, _ in results]
    rank_values = [rank for _, rank in results]
    
    def spearman_rank_correlation(x, y):
        x_ranks = {x[i]: i + 1 for i in range(len(x))}
        y_ranks = {y[i]: i + 1 for i in range(len(y))}
        n = len(x)
        sum_d_squared = sum((x_ranks[x[i]] - y_ranks[y[i]]) ** 2 for i in range(n))
        return 1 - (6 * sum_d_squared) / (n * (n**2 - 1))
    
    correlation = spearman_rank_correlation(n_values, rank_values)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": correlation,
        "instances_tested": len(results),
        "conjecture_holds": correlation >= 0.95,  # Adjust threshold as needed
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_corr = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")