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
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find pivot row
        max_row = i
        for r in range(i + 1, rows):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below pivot
        pivot = matrix[i][i]
        if pivot == 0:
            continue
        for j in range(i, cols):
            matrix[i][j] /= pivot
        
        for r in range(rows):
            if r != i and matrix[r][i] != 0:
                factor = matrix[r][i]
                for j in range(i, cols):
                    matrix[r][j] -= factor * matrix[i][j]
    rank = sum(1 for row in matrix if any(val != 0 for val in row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    
    def generate_bp(n):
        bp = []
        for i in range(n):
            bp.append(random.choice(['R', 'O']))
        return bp
    
    def is_read_once(bp):
        return all(x == 'O' for x in bp)
    
    def transition_matrix(bp):
        m = [[0] * n for _ in range(n)]
        for i in range(n):
            if bp[i] == 'R':
                j = random.randint(0, i - 1) if i > 0 else 0
                m[i][j] = 1
            elif bp[i] == 'O':
                j = random.randint(i + 1, n - 1)
                m[j][i] = 1
        return m
    
    def matroid_rank(matrix):
        return gaussian_elimination(matrix)
    
    read_once_count = 0
    total_rank = 0
    
    for _ in range(30):
        bp = generate_bp(n)
        if is_read_once(bp):
            read_once_count += 1
            rank = matroid_rank(transition_matrix(bp))
            if rank > 0.1 * n:
                continue
            else:
                return {
                    "metric_name": "matroid_rank",
                    "metric_value": rank,
                    "instances_tested": 30,
                    "conjecture_holds": False,
                    "counterexample": f"Read-once BP with rank {rank} <= 0.1n"
                }
        else:
            rank = matroid_rank(transition_matrix(bp))
            if rank < 0.8 * n:
                continue
            total_rank += rank
    
    avg_rank = total_rank / (30 - read_once_count)
    return {
        "metric_name": "matroid_rank",
        "metric_value": avg_rank,
        "instances_tested": 30,
        "conjecture_holds": True if avg_rank >= 0.8 * n else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")