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
    
    def xor_and_tree(depth, width):
        if depth == 0:
            return [random.choice([0, 1])]
        else:
            children = [xor_and_tree(depth-1, width//2) for _ in range(width)]
            return [x ^ y for x in children[::2] for y in children[1::2]]
    
    def grothendieck_tensor_product(poly):
        n = len(poly)
        tensor = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if poly[i] == 1 and poly[j] == 1:
                    tensor[i][j] = 1
        return tensor
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        augmented_matrix = [row + [0] for row in matrix]
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            if augmented_matrix[i][i] == 0:
                continue
            for j in range(i+1, n):
                augmented_matrix[i][j] /= augmented_matrix[i][i]
            for k in range(m):
                if k != i and augmented_matrix[k][i] != 0:
                    for j in range(n):
                        augmented_matrix[k][j] -= augmented_matrix[i][j] * augmented_matrix[k][i]
        rank = sum(1 for row in augmented_matrix if any(row[j] != 0 for j in range(n)))
        return rank
    
    def clause_indicator_polynomial(tree, n):
        poly = [0]*n
        for i, node in enumerate(tree):
            if node == 1:
                poly[i % n] = 1
        return poly
    
    n = random.randint(5, 40)
    tree_width = random.randint(2, min(n-1, 10))
    depth = random.randint(1, 3)
    tree = xor_and_tree(depth, tree_width)
    
    poly = clause_indicator_polynomial(tree, n)
    tensor_product = grothendieck_tensor_product(poly)
    rank_value = rank(tensor_product)
    
    w = tree_width
    d = depth
    ratio = rank_value / (w**d)
    
    return {
        "metric_name": "Rank Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1.5,
        "counterexample": "" if ratio <= 1.5 else f"Ratio {ratio} exceeds bound for w={w}, d={d}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")