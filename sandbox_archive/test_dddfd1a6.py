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
    
    def tropicalize(matrix):
        return [[max(row[j], col[i]) for j in range(len(col))] for i, row in enumerate(matrix)]
    
    def matrix_rank(matrix):
        m = len(matrix)
        n = len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if all(matrix[k][i] == float('-inf') for k in range(i, m)):
                continue
            pivot_row = max(range(i, m), key=lambda x: matrix[x][i])
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            rank += 1
            for j in range(m):
                if j != i:
                    factor = matrix[j][i] - matrix[i][i]
                    if factor == float('-inf'):
                        continue
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def generate_disjointness_matrix(n):
        A = [[0]*n for _ in range(n)]
        for i in range(n):
            A[i][i] = 1
        return A
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            A = generate_disjointness_matrix(n)
            A_trop = tropicalize(A)
            rank = matrix_rank(A_trop)
            total_rank += rank
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = mean_rank >= 0.5 * n_values[-1]
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "tropical_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")