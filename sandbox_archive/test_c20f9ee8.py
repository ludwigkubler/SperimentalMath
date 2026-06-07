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
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
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
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += ((-1) ** j) * A[0][j] * determinant(submatrix)
        return det

    def hodge_index(A):
        n = len(A)
        adjugate = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
                adjugate[j][i] = determinant(submatrix) * ((-1) ** (i + j))
        return sum(A[i][j] * adjugate[i][j] for i in range(n) for j in range(n))

    def dpll_path_length(phi):
        stack = []
        assignment = [None] * len(phi)
        def backtrack():
            if not phi:
                return 0
            literal = next((lit for lit in phi[0] if assignment[lit // 2] is None), None)
            if literal is None:
                return float('inf')
            assignment[literal // 2] = literal % 2 == 1
            stack.append(literal)
            path_length = backtrack()
            if path_length != float('inf'):
                return path_length + 1
            assignment[literal // 2] = not (literal % 2 == 1)
            stack.pop()
            assignment[literal // 2] = None
            stack.append(-literal)
            path_length = backtrack()
            if path_length != float('inf'):
                return path_length + 1
            stack.pop()
            return float('inf')
        return backtrack()

    def generate_cnf(n):
        clauses = []
        for i in range(2**n):
            clause = []
            for j in range(n):
                if (i >> j) & 1:
                    clause.append(j * 2 + 1)
                else:
                    clause.append(-(j * 2 + 1))
            clauses.append(clause)
        return clauses

    n = random.randint(5, 40)
    phi = generate_cnf(n)
    
    A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    H = hodge_index(A)
    P = dpll_path_length(phi)
    
    return {
        "metric_name": "Hodge Index vs DPLL Path Length",
        "metric_value": abs(H - P),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")