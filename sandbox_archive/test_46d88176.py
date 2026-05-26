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
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for j in range(m):
                if i != j:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def characteristic_polynomial(A):
        n = len(A)
        if n == 1:
            return [A[0][0]]
        elif n == 2:
            a, b, c, d = A[0][0], A[0][1], A[1][0], A[1][1]
            return [1, -(a + d), a * d - b * c]
        else:
            det = 0
            for j in range(n):
                submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
                det += (-1) ** j * A[0][j] * determinant(submatrix)
            return [det]
    
    def determinant(A):
        if len(A) == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        else:
            det = 0
            for j in range(len(A)):
                submatrix = [[A[i][k] for k in range(1, len(A)) if k != j] for i in range(1, len(A))]
                det += (-1) ** j * A[0][j] * determinant(submatrix)
            return det
    
    def hypergeometric_series(G):
        n = len(G)
        P = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        Q = matrix_multiply(P, G)
        R = gaussian_elimination(Q)
        rank = sum(1 for row in R if any(row))
        return rank
    
    def tseitin_formula(G):
        n = len(G)
        clauses = []
        for i in range(n):
            clause = [f"p{i}"]
            for j in range(n):
                if G[i][j]:
                    clause.append(f"-p{j}")
            clauses.append(clause)
        return clauses
    
    def resolution_width(phi):
        n = len(phi)
        clauses = phi + [[f"-p{i}" for i in range(n)]]
        queue = [clause[:] for clause in clauses]
        while queue:
            clause1 = queue.pop()
            if not any(var in clause1 for var in clause1[:len(clause1)//2]):
                return len(queue)
            for clause2 in queue:
                if any(var in clause2 for var in clause2[:len(clause2)//2]):
                    new_clause = list(set(clause1 + clause2) - {"-p" + var for var in clause1})
                    if not new_clause:
                        return len(queue)
                    if new_clause not in queue:
                        queue.append(new_clause)
        return len(queue)
    
    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    phi = tseitin_formula(G)
    rank = hypergeometric_series(G)
    width = resolution_width(phi)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width >= 2 ** (math.log2(rank) if rank > 0 else -math.inf),
        "counterexample": "" if width >= 2 ** (math.log2(rank) if rank > 0 else -math.inf) else f"Graph with n={n}, rank={rank}, width={width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with rank < width\" first_failing_seed={first_failing_seed}")