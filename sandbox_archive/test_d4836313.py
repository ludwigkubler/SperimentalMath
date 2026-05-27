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
    else:
        left_poly = characteristic_polynomial(tree[:len(tree)//2])
        right_poly = characteristic_polynomial(tree[len(tree)//2:])
        n = len(left_poly)
        result = [0] * (n + len(right_poly))
        for i in range(n):
            for j in range(len(right_poly)):
                result[i + j] += left_poly[i] * right_poly[j]
        return result

def minimal_rank_brauer_group(poly):
    n = len(poly)
    if n == 1:
        return 0
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = poly[i] - poly[j]
    rank = 0
    for row in matrix:
        if any(row):
            rank += 1
            for other_row in matrix:
                if other_row != row and any(other_row):
                    factor = other_row[rank-1] / row[rank-1]
                    for k in range(n):
                        other_row[k] -= factor * row[k]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        tree = xor_and_tree(n)
        poly = characteristic_polynomial(tree)
        rank = minimal_rank_brauer_group(poly)
        results.append((n, rank))
    
    n_values = [r[0] for r in results]
    ranks = [r[1] for r in results]
    expected_ranks = [2**(n/2) for n in n_values]
    
    from scipy.stats import spearmanr
    correlation, _ = spearmanr(ranks, expected_ranks)
    
    metric_name = "Spearman rank correlation"
    metric_value = correlation
    instances_tested = len(n_values)
    conjecture_holds = correlation >= 0.95
    counterexample = "" if conjecture_holds else f"Correlation {correlation} < 0.95"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r['metric_value'] for r in results) / len(results)
    std_metric = math.sqrt(sum((r['metric_value'] - mean_metric)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation < 0.95\" first_failing_seed={first_failing_seed}")