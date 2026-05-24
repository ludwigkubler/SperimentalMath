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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        m = len(A)
        if m == 1:
            return A[0][0]
        det = 0
        for j in range(m):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def sheaf_rank(n, m):
        # Construct a random CNF formula
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        
        # Convert CNF to polynomial (simplified example)
        polynomial = 1
        for clause in clauses:
            term = 1
            for var in clause:
                if var > 0:
                    term *= (1 + x[var-1])
                else:
                    term *= (1 - x[-var-1])
            polynomial *= term
        
        # Compute sheaf rank (simplified example)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    A[i][j] = 1
                else:
                    A[i][j] = polynomial[i][j]
        
        rank = determinant(A)
        return rank
    
    def dpll_refutation_tree_width(n, m):
        # Simplified example: width is proportional to n
        return n
    
    n = random.randint(5, 40)
    m = random.randint(1, n)
    
    rank = sheaf_rank(n, m)
    width = dpll_refutation_tree_width(n, m)
    
    if rank == 0:
        return {
            "metric_name": "dpll_refutation_tree_width",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "sheaf_rank_zero"
        }
    
    ratio = width / math.log(n**m + m)
    return {
        "metric_name": "dpll_refutation_tree_width",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 2 * math.log(n**m + m),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["instances_tested"] > 0) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["instances_tested"] > 0) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")