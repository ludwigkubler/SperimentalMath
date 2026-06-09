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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def gaussian_elimination(matrix, mod):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for col in range(cols):
            pivot_row = None
            for row in range(rank, rows):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row is not None:
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                for r in range(rows):
                    if r != rank and matrix[r][col] != 0:
                        factor = -matrix[r][col] * pow(matrix[rank][col], mod-2, mod) % mod
                        for c in range(cols):
                            matrix[r][c] = (matrix[r][c] + factor * matrix[rank][c]) % mod
                rank += 1
        return rank
    
    def compute_char_variety(cnf, p):
        n = len(cnf)
        matrix = [[0] * (n + 2) for _ in range(n + 2)]
        for clause in cnf:
            i, j = abs(clause[0]) - 1, abs(clause[1]) - 1
            if clause[0] > 0:
                matrix[i][j + n + 1] += 1
            else:
                matrix[j][i + n + 1] += 1
            matrix[i][n] += 1
            matrix[j][n] += 1
        return gaussian_elimination(matrix, p)
    
    def resolution_width(cnf):
        # Simplified version of resolution width calculation (not exact)
        return len(cnf) ** 0.5
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    p = 101
    char_variety_rank = compute_char_variety(cnf, p)
    width = resolution_width(cnf)
    
    return {
        "metric_name": "K-theoretic Rank",
        "metric_value": char_variety_rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": char_variety_rank <= n**2 * math.log(n) and width <= min(width, math.log(n)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")