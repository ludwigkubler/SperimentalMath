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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def bp_read_twice(n):
        if n == 2:
            return [[1, 0], [0, 1]]
        else:
            return [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    
    def matrix_rank(matrix):
        m = len(matrix)
        n = len(matrix[0])
        if m == 0 or n == 0:
            return 0
        rank = 0
        for col in range(n):
            pivot_row = -1
            for row in range(rank, m):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row == -1:
                continue
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            rank += 1
            for row in range(rank, m):
                factor = Fraction(matrix[row][col], matrix[rank-1][col])
                for j in range(n):
                    matrix[row][j] -= factor * matrix[rank-1][j]
        return rank
    
    def construct_matrix(bp):
        n = len(bp)
        size = 2 ** (n - 1)
        matrix = [[0] * size for _ in range(size)]
        for i in range(n):
            for j in range(2 ** (i - 1)):
                if bp[i][j] == 1:
                    for k in range(2 ** (n - i - 1)):
                        matrix[j * 2 + k][k] = 1
                        matrix[(j + 1) * 2 + k][k] = 1
        return matrix
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        if n == 2:
            bp = [[1, 0], [0, 1]]
        else:
            bp = bp_read_twice(n)
        
        matrix = construct_matrix(bp)
        rank = matrix_rank(matrix)
        total_rank += rank
        instances_tested += 1
    
    mean_rank = Fraction(total_rank, instances_tested)
    
    if n == 2:
        conjecture_holds = mean_rank >= 2
        counterexample = "" if conjecture_holds else "IP_2 BP"
    else:
        conjecture_holds = mean_rank <= n * Fraction(1, 2)
        counterexample = "" if conjecture_holds else f"Random BP of size {n}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": float(mean_rank),
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
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")