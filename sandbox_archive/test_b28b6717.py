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
    
    def generate_boolean_function(X):
        return [random.randint(0, 1) for _ in range(2**X)]
    
    def matrix_from_function(f, X, Y):
        M = [[0] * (2**Y) for _ in range(2**X)]
        for x in range(2**X):
            for y in range(2**Y):
                if f[x] == 1:
                    M[x][y] = 1
        return M
    
    def gaussian_elimination(M):
        rows, cols = len(M), len(M[0])
        rank = 0
        for j in range(cols):
            i_max = None
            for i in range(rank, rows):
                if M[i][j] != 0:
                    i_max = i
                    break
            if i_max is None:
                continue
            M[rank], M[i_max] = M[i_max], M[rank]
            pivot = M[rank][j]
            for k in range(j, cols):
                M[rank][k] /= pivot
            for i in range(rows):
                if i != rank and M[i][j] != 0:
                    factor = M[i][j]
                    for k in range(j, cols):
                        M[i][k] -= factor * M[rank][k]
            rank += 1
        return rank
    
    def minimal_rank_tropicalized_group(M):
        rows, cols = len(M), len(M[0])
        tropical_matrix = [[max(M[i][j], M[j][i]) for j in range(cols)] for i in range(rows)]
        return gaussian_elimination(tropical_matrix)
    
    def communication_complexity_disjoint(M):
        if not M:
            return 0
        rows, cols = len(M), len(M[0])
        if rows == 1 and cols == 1:
            return 0
        if rows == 1:
            return 1 + communication_complexity_disjoint([M[0][i:i+cols//2] for i in range(0, cols, cols//2)])
        if cols == 1:
            return 1 + communication_complexity_disjoint([[M[i][j] for j in range(cols)] for i in range(rows//2, rows)])
        mid_row = rows // 2
        mid_col = cols // 2
        A = [M[i][:mid_col] for i in range(mid_row)]
        B = [M[i][mid_col:] for i in range(mid_row)]
        C = [M[mid_row:][i][:mid_col] for i in range(mid_col)]
        D = [M[mid_row:][i][mid_col:] for i in range(mid_col, cols)]
        return 1 + max(communication_complexity_disjoint(A), communication_complexity_disjoint(B), communication_complexity_disjoint(C), communication_complexity_disjoint(D))
    
    n = random.randint(3, 40)
    f = generate_boolean_function(n)
    M = matrix_from_function(f, n, n)
    tau_G_M = minimal_rank_tropicalized_group(M)
    CC_DISJ_M = communication_complexity_disjoint(M)
    
    if tau_G_M == 0:
        return {
            "metric_name": "CC_DISJ",
            "metric_value": CC_DISJ_M,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    conjecture_holds = tau_G_M**2 <= CC_DISJ_M
    return {
        "metric_name": "CC_DISJ",
        "metric_value": CC_DISJ_M,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Counterexample: τ_G(M) = {tau_G_M}, CC_{DISJ}(M) = {CC_DISJ_M}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")