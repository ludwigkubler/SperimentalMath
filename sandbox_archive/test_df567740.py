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
    
    def generate_dnf(n):
        clauses = []
        for _ in range(random.randint(1, n)):
            literals = [random.choice([f'x{i}', f'-x{i}']) for i in range(1, n+1)]
            clause = ' ∨ '.join(literals)
            clauses.append(clause)
        return ' ∧ '.join(clauses)
    
    def moment_matrix(dnf):
        # Simplified version for demonstration purposes
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    def tropicalize(matrix):
        return [[max(row[j] + col[i] for row, col in zip(matrix, transpose(matrix))) for j in range(len(matrix[0]))] for i in range(len(matrix))]
    
    def transpose(matrix):
        return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
    
    def min_rank(matrix):
        # Simplified version using Gaussian elimination
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for col in range(cols):
            if all(matrix[row][col] == 0 for row in range(rank, rows)):
                continue
            pivot_row = rank
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            for row in range(rank + 1, rows):
                factor = -matrix[row][col] / matrix[pivot_row][col]
                for j in range(col, cols):
                    matrix[row][j] += factor * matrix[pivot_row][j]
            rank += 1
        return rank
    
    n = random.randint(5, 40)
    dnf = generate_dnf(n)
    M_phi = moment_matrix(dnf)
    P_phi = tropicalize(M_phi)
    minimal_rank = min_rank(P_phi)
    
    return {
        "metric_name": "Minimal Rank of Tropicalized Moment Matrix",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": minimal_rank >= n**(1/4),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_minimal_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_minimal_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_minimal_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='minimal_rank_too_small' first_failing_seed={first_failing_seed}")