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
            left = xor_and_tree(depth - 1, width // 2)
            right = xor_and_tree(depth - 1, width // 2)
            return [l ^ r for l in left for r in right]
    
    def polynomial(f):
        n = len(f)
        poly = [[0] * (n + 1) for _ in range(n + 1)]
        poly[0][0] = 1
        for i in range(1, n + 1):
            poly[i][0] = -f[i - 1]
            for j in range(1, i + 1):
                poly[i][j] = poly[i - 1][j - 1] ^ poly[i - 1][j]
        return poly
    
    def grothendieck_tensor_product(poly1, poly2):
        n = len(poly1)
        m = len(poly2)
        result = [[0] * (n + m) for _ in range(n + m)]
        for i in range(n):
            for j in range(m):
                for k in range(n + m):
                    result[i + j][k] ^= poly1[i][j] & poly2[k - j]
        return result
    
    def rank(matrix):
        n = len(matrix)
        m = len(matrix[0])
        row, col = 0, 0
        while row < n and col < m:
            if matrix[row][col] == 0:
                for i in range(row + 1, n):
                    if matrix[i][col] != 0:
                        matrix[row], matrix[i] = matrix[i], matrix[row]
                        break
                else:
                    col += 1
                    continue
            pivot = matrix[row][col]
            for j in range(col, m):
                matrix[row][j] ^= pivot
            for i in range(n):
                if i != row and matrix[i][col] != 0:
                    factor = matrix[i][col]
                    for j in range(col, m):
                        matrix[i][j] ^= factor & matrix[row][j]
            row += 1
            col += 1
        return min(row, col)
    
    def clause_indicator_polynomial(tree):
        n = len(tree)
        poly = [0] * (n + 1)
        for i in range(n):
            if tree[i] == 1:
                poly[0] ^= 1
                for j in range(1, n + 1):
                    poly[j] ^= poly[j - 1]
        return poly
    
    def negate_polynomial(poly):
        return [1 ^ x for x in poly]
    
    depth = random.randint(2, 4)
    width = 2 ** depth
    tree = xor_and_tree(depth, width)
    f = clause_indicator_polynomial(tree)
    g = negate_polynomial(f)
    
    poly_f = polynomial(f)
    poly_g = polynomial(g)
    tensor_product = grothendieck_tensor_product(poly_f, poly_g)
    
    rank_value = rank(tensor_product)
    w_d = width ** depth
    
    return {
        "metric_name": "Ratio of Rank to w^d",
        "metric_value": rank_value / w_d,
        "instances_tested": 1,
        "conjecture_holds": rank_value <= 1.5 * w_d,
        "counterexample": "" if rank_value <= 1.5 * w_d else "Rank exceeds 1.5 * w^d"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(3, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = len(results) / len(seeds)
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds 1.5 * w^d\" first_failing_seed={first_failing_seed}")