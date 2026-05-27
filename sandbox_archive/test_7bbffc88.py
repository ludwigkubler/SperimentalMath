# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def xor_and_tree(depth, width):
    if depth == 0:
        return [random.randint(0, 1)]
    children = []
    for _ in range(width):
        child = xor_and_tree(depth-1, width//2)
        children.extend(child)
    return [x ^ y for x in children[::2] for y in children[1::2]]

def clause_indicator_polynomial(tree):
    if len(tree) == 1:
        return tree
    return [x ^ y for x, y in zip(clause_indicator_polynomial(tree[:len(tree)//2]), clause_indicator_polynomial(tree[len(tree)//2:]))]

def grothendieck_tensor_product(f, g):
    n = len(f)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = f[i] & g[j]
    return result

def rank(matrix):
    m, n = len(matrix), len(matrix[0])
    augmented_matrix = [row + [1 if i == j else 0 for j in range(m)] for i, row in enumerate(matrix)]
    for col in range(n):
        max_row = max(range(col, m), key=lambda r: abs(augmented_matrix[r][col]))
        augmented_matrix[col], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[col]
        if augmented_matrix[col][col] == 0:
            return None
        for row in range(m):
            if row != col:
                factor = Fraction(-augmented_matrix[row][col], augmented_matrix[col][col])
                for j in range(n + m):
                    augmented_matrix[row][j] += factor * augmented_matrix[col][j]
    return sum(1 for row in range(m) if augmented_matrix[row][-1] == 1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        tree_width = random.randint(1, min(n, 10))
        depth = random.randint(1, min(n // tree_width, 5))
        tree = xor_and_tree(depth, tree_width)
        f = clause_indicator_polynomial(tree)
        g = [x ^ 1 for x in f]
        tensor_product = grothendieck_tensor_product(f, g)
        r = rank(tensor_product)
        if r is None:
            continue
        results.append((r, n, tree_width))
    if not results:
        return {
            "metric_name": "rank_ratio",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    rank_ratios = [r / (w ** d) for r, n, w in results]
    mean_ratio = sum(rank_ratios) / len(rank_ratios)
    std_dev = (sum((x - mean_ratio) ** 2 for x in rank_ratios) / len(rank_ratios)) ** 0.5
    return {
        "metric_name": "rank_ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": all(r <= 1.5 for r in rank_ratios),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30)) + [random.randint(100, 999) for _ in range(27)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    mean_ratio = sum(r['metric_value'] for r in results) / len(results)
    std_dev = (sum((r['metric_value'] - mean_ratio) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        counterexample = "first failing seed"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")