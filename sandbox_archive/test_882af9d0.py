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

def gaussian_elimination(matrix):
    n = len(matrix)
    rank = 0
    for col in range(n):
        pivot_row = None
        for row in range(rank, n):
            if matrix[row][col] != 0:
                pivot_row = row
                break
        if pivot_row is None:
            continue
        rank += 1
        for row in range(n):
            if row != pivot_row:
                factor = -matrix[row][col] / matrix[pivot_row][col]
                for j in range(col, n):
                    matrix[row][j] += factor * matrix[pivot_row][j]
    return rank

def k_clique_rank(I):
    n = len(I)
    I_matrix = [[0] * n for _ in range(n)]
    for u in range(n):
        for v in range(u + 1, n):
            if (u, v) in I or (v, u) in I:
                I_matrix[u][v] = 1
                I_matrix[v][u] = 1
    return gaussian_elimination(I_matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    vertices = list(range(n))
    edges = set()
    for _ in range(random.randint(int(n * (n - 1) / 2), int(n * (n - 1) / 2))):
        u, v = random.sample(vertices, 2)
        if u < v:
            edges.add((u, v))
    
    I = {(u, v) for u in vertices for v in vertices if (u, v) in edges or (v, u) in edges}
    
    rank = k_clique_rank(I)
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank >= math.sqrt(n)
    counterexample = "" if conjecture_holds else f"Rank {rank} < sqrt({n})"
    
    return {
        "metric_name": "affine_representation_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")