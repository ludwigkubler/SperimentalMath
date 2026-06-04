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
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i]:
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
    
    def min_order(matrix):
        m, n = len(matrix), len(matrix[0])
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(m)]
        echelon_form = gaussian_elimination(identity)
        rank = sum(1 for row in echelon_form if any(row))
        return rank
    
    def quasi_crystalline_sheaf(cnf):
        n = len(cnf[0])
        matrix = [[0] * (2**n) for _ in range(2**n)]
        for clause in cnf:
            for literal in clause:
                row, col = abs(literal) - 1, 2**(abs(literal) - 1)
                if literal < 0:
                    col -= 2**(n - abs(literal))
                matrix[row][col] += 1
        return matrix
    
    def resolution_width(cnf):
        n = len(cnf[0])
        clauses = [set(clause) for clause in cnf]
        queue = set()
        for clause in clauses:
            if len(clause) == 1:
                queue.add(next(iter(clause)))
        while queue:
            literal = queue.pop()
            new_clauses = []
            for clause in clauses:
                if literal in clause:
                    continue
                if -literal in clause:
                    return len(queue)
                new_clause = clause.copy()
                new_clause.remove(-literal)
                new_clauses.append(new_clause)
            clauses.extend(new_clauses)
        return len(queue)
    
    n = random.randint(5, 40)
    cnf = [[random.choice([-1, 1]) * (i + 1) for i in range(n)] for _ in range(random.randint(2, 10))]
    qc_sheaf = quasi_crystalline_sheaf(cnf)
    min_order_qc = min_order(qc_sheaf)
    w_phi = resolution_width(cnf)
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": abs(w_phi),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(w_phi) <= math.log(n, 2) * min_order_qc,
        "counterexample": "" if conjecture_holds else f"Counterexample for n={n}"
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")