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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] == -clause[j] for i in range(n) for j in range(i+1, n)):
                continue
            clauses.append(clause)
        return clauses
    
    def gram_matrix(cnf):
        n = len(cnf[0])
        G = [[0] * n for _ in range(n)]
        for clause in cnf:
            for i in range(n):
                for j in range(i, n):
                    G[i][j] += clause[i] * clause[j]
                    if i != j:
                        G[j][i] = G[i][j]
        return G
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for col in range(n):
            pivot_row = -1
            for row in range(rank, m):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row == -1:
                continue
            rank += 1
            for i in range(m):
                if i != pivot_row:
                    factor = matrix[i][col] / matrix[pivot_row][col]
                    for j in range(n):
                        matrix[i][j] -= factor * matrix[pivot_row][j]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = int(0.5 * n * (n - 1))  # Ensure at least one clause
        cnf = generate_cnf(n, m)
        G = gram_matrix(cnf)
        rank = matrix_rank(G)
        results.append({
            "metric_name": "minimal_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": rank <= 3 * n**2 / m and rank <= 10 * n**2 / m,
            "counterexample": "" if rank <= 10 * n**2 / m else f"min_rank > 10n^2/m"
        })
    
    return results[0]

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")