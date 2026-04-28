# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math

def xor_tree(n):
    if n == 1:
        return [0, 1]
    left = xor_tree(n // 2)
    right = xor_tree(n // 2)
    return [left[i] ^ right[i] for i in range(n)]

def depth_bounded_distinguisher(tree, x, y, R):
    queue = [(x, 0)]
    visited = set()
    while queue:
        node, d = queue.pop(0)
        if node == y or d > R:
            continue
        visited.add(node)
        for i in range(len(tree)):
            if tree[i] == node and i not in visited:
                queue.append((i, d + 1))
    return len(visited)

def build_cochain_spaces(tree, R):
    n = len(tree)
    C0 = [[0] * (n * n) for _ in range(n)]
    C1 = [[0] * (n * n) for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if depth_bounded_distinguisher(tree, i, j, R) <= R:
                C0[i][j] = 1
                C1[i][j] = 1
    return C0, C1

def smith_normal_form(matrix):
    n = len(matrix)
    for k in range(n):
        pivot_row = k + max(range(k, n), key=lambda r: abs(matrix[r][k]))
        matrix[k], matrix[pivot_row] = matrix[pivot_row], matrix[k]
        for i in range(n):
            if i != k:
                factor = matrix[i][k] / matrix[k][k]
                for j in range(n):
                    matrix[i][j] -= factor * matrix[k][j]
    return matrix

def rank_over_Q(matrix):
    n = len(matrix)
    rank = 0
    for k in range(n):
        if matrix[k][k] != 0:
            rank += 1
            for i in range(n):
                if i != k:
                    factor = matrix[i][k] / matrix[k][k]
                    for j in range(k, n):
                        matrix[i][j] -= factor * matrix[k][j]
    return rank

def build_roe_operator(tree, R):
    n = len(tree)
    T = [[0] * (n * n) for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if depth_bounded_distinguisher(tree, i, j, R) <= R:
                T[i][j] = random.choice([-1, 1])
    return T

def trace_pairing(c, T):
    n = len(c)
    return sum(c[i][j] * T[i][j] for i in range(n) for j in range(n))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [4, 8, 16, 32]:
        tree = xor_tree(n)
        R_max = math.floor(0.5 * math.log2(n))
        HX1_R_values = []
        
        for R in range(1, 2 * math.log2(n) + 1):
            C0, C1 = build_cochain_spaces(tree, R)
            delta_0 = [[C0[i][j] - C0[j][i] for j in range(n)] for i in range(n)]
            delta_1 = [[C1[i][j] - C1[j][i] for j in range(n)] for i in range(n)]
            SNF_delta_1 = smith_normal_form(delta_1)
            rank_HX1_R = rank_over_Q(SNF_delta_1)
            HX1_R_values.append(rank_HX1_R)
        
        if max(HX1_R_values[:R_max]) == 0 and min(HX1_R_values[R_max:]) > 0:
            slope, intercept = 0, 0
            for R, rank in zip(range(1, 2 * math.log2(n) + 1), HX1_R_values):
                slope += (math.log(rank) - math.log(math.log2(n))) / math.log(R)
                intercept += (math.log(rank) - math.log(math.log2(n)) - slope * math.log(R))
            slope /= len(HX1_R_values)
            intercept /= len(HX1_R_values)
            
            results.append({
                "n": n,
                "slope": slope,
                "intercept": intercept
            })
    
    if all(result["slope"] >= math.log2(n) - 2 for result in results):
        return {
            "metric_name": "Slope",
            "metric_value": sum(result["slope"] for result in results) / len(results),
            "instances_tested": len(results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        counterexample = f"Slope not consistent with conjecture for n={results[0]['n']}"
        return {
            "metric_name": "Slope",
            "metric_value": sum(result["slope"] for result in results) / len(results),
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": counterexample
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_slope = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["slope"] >= math.log2(n) - 2 for n, r in zip([4, 8, 16, 32], results)):
        print(f"RESULT: SUPPORTED mean={mean_slope} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Slope not consistent with conjecture\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE slope_not_consistent_with_conjecture")