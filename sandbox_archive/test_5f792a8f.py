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
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
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
        if m == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def minimal_rank(A):
        rank = 0
        while A:
            pivot_row = next((i for i, row in enumerate(A) if any(row)), None)
            if pivot_row is None:
                break
            A[pivot_row], A[0] = A[0], A[pivot_row]
            pivot_col = next(i for i, val in enumerate(A[0]) if val != 0)
            rank += 1
            for row in A[1:]:
                factor = row[pivot_col] / A[0][pivot_col]
                row[:] = [x - factor * y for x, y in zip(row, A[0])]
        return rank

    def dpll_width(clauses):
        if not clauses:
            return 0
        variables = set()
        for clause in clauses:
            variables.update(clause)
        max_width = 0
        for var in variables:
            positive_clauses = [clause for clause in clauses if var in clause]
            negative_clauses = [clause for clause in clauses if -var in clause]
            width = max(dpll_width(positive_clauses), dpll_width(negative_clauses))
            max_width = max(max_width, width + 1)
        return max_width

    def generate_random_sat_instance(n):
        variables = list(range(-n, n+1))
        clauses = []
        for _ in range(n * (n + 1) // 2):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses

    def clause_indicator_polynomial(clauses, variables):
        m = len(clauses)
        n = len(variables)
        A = [[0] * (n + 1) for _ in range(m)]
        for i, clause in enumerate(clauses):
            for var in clause:
                if var > 0:
                    A[i][var - 1] += 1
                else:
                    A[i][-1] -= 1
        return A

    n = random.randint(5, 40)
    clauses = generate_random_sat_instance(n)
    variables = list(range(-n, n+1))
    polynomial = clause_indicator_polynomial(clauses, variables)

    rank = minimal_rank(polynomial)
    width = dpll_width(clauses)

    f_n = math.sqrt(n) * math.log(n)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= f_n,
        "counterexample": "" if rank <= f_n else f"rank={rank} > Θ(√{n} log {n}) = {f_n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeds Θ(√n log n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")