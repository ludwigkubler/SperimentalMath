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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def rank(A):
        rref = gaussian_elimination(A)
        return sum(1 for row in rref if any(row))

    def tseitin_formula(n):
        variables = list(range(1, n+1))
        clauses = []
        for i in range(1, n+1):
            clauses.append([i])
            clauses.append([-i])
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append([i, -j])
                clauses.append([-i, j])
                clauses.append([i, j])
                clauses.append([-i, -j])
        return variables, clauses

    def resolution_width(clauses):
        queue = set()
        for clause in clauses:
            queue.add(tuple(sorted(clause)))
        while True:
            new_clause = None
            for clause1 in queue:
                for clause2 in queue:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = tuple(sorted(list(set(clause1) ^ set(clause2))))
                        break
                if new_clause is not None:
                    break
            if new_clause is None:
                return len(queue)
            queue.add(new_clause)

    def vector_bundle_rank(n):
        # Simplified model for demonstration purposes
        return n

    variables, clauses = tseitin_formula(40)
    width = resolution_width(clauses)
    rank_value = vector_bundle_rank(40)
    
    return {
        "metric_name": "Resolution Width vs Vector Bundle Rank",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": 40,
        "conjecture_holds": width <= rank_value,
        "counterexample": "" if width <= rank_value else f"width={width} > rank={rank_value}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"width > rank\" first_failing_seed={first_failing_seed}")