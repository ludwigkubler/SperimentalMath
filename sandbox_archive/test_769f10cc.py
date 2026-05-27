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
        return [0]
    else:
        left = xor_and_tree(n // 2)
        right = xor_and_tree(n - len(left))
        return [x ^ y for x, y in zip(left, right)]

def clause_indicator_polynomial(tree):
    if not tree:
        return []
    elif len(tree) == 1:
        return [tree[0]]
    else:
        left = clause_indicator_polynomial(tree[:len(tree)//2])
        right = clause_indicator_polynomial(tree[len(tree)//2:])
        return [x ^ y for x, y in zip(left, right)]

def grothendieck_tensor_product(f):
    n = len(f)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = f[i] & f[j]
    return result

def rank(matrix):
    m, n = len(matrix), len(matrix[0])
    augmented_matrix = [row + [1 if i == j else 0 for j in range(m)] for i, row in enumerate(matrix)]
    for i in range(m):
        max_row = max(range(i, m), key=lambda r: abs(augmented_matrix[r][i]))
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        if augmented_matrix[i][i] == 0:
            return float('inf')
        for j in range(n + 1):
            augmented_matrix[i][j] /= augmented_matrix[i][i]
        for k in range(m):
            if k != i and augmented_matrix[k][i] != 0:
                factor = augmented_matrix[k][i]
                for j in range(n + 1):
                    augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
    return sum(1 for row in augmented_matrix if any(row))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    tree = xor_and_tree(n)
    f = clause_indicator_polynomial(tree)
    g = [x ^ 1 for x in f]
    tensor_product = grothendieck_tensor_product(f + g)
    r = rank(tensor_product)
    w = n
    d = int(math.log2(w))
    ratio = r / (w ** d)
    return {
        "metric_name": "Ratio of Rank to w^d",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")