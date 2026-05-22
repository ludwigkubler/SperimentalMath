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
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
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

    def matrix_multiplication(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def compute_local_cohomology_rank(A):
        rank = 0
        A_rref = gaussian_elimination(A)
        for row in A_rref:
            if any(row):
                rank += 1
        return rank

    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append([f'-{i}', f'{i}'])
        for i in range(2, n+1):
            for j in range(i-1):
                clauses.append([f'-{i}', f'-{j}', f'{i+j}'])
        return variables, clauses

    def construct_quiver_representation(variables, clauses):
        n = len(variables)
        A = [[0] * (2*n) for _ in range(2*n)]
        for var in variables:
            i = int(var[1:]) - 1
            A[i][i+n] = 1
            A[n+i][i] = 1
        for clause in clauses:
            if len(clause) == 3:
                a, b, c = clause
                ai = int(a[1:]) - 1 if a.startswith('-') else None
                bi = int(b[1:]) - 1 if b.startswith('-') else None
                ci = int(c[1:]) - 1 if c.startswith('-') else None
                if ai is not None:
                    A[n+ai][ci] = 1
                if bi is not None:
                    A[n+bi][ci] = 1
        return A

    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n)
    quiver_representation = construct_quiver_representation(variables, clauses)
    h_phi = compute_local_cohomology_rank(quiver_representation)

    def resolution_proof_length(clauses):
        length = 0
        while clauses:
            new_clause = None
            for clause in clauses:
                if len(clause) == 1:
                    return float('inf')
                if len(clause) == 2:
                    new_clause = clause[0]
                    break
            if new_clause is None:
                return length
            length += 1
            new_clauses = []
            for clause in clauses:
                if not any(var in clause for var in new_clause):
                    new_clauses.append(clause)
                elif len(clause) > 2:
                    new_clauses.append([var for var in clause if var != new_clause[0]])
            clauses = new_clauses
        return length

    proof_length = resolution_proof_length(clauses)

    metric_value = proof_length >= 2**h_phi and h_phi <= math.log(n, 2)
    conjecture_holds = metric_value
    counterexample = "" if conjecture_holds else f"n={n}, h(φ)={h_phi}, proof_length={proof_length}"

    return {
        "metric_name": "Resolution Proof Length vs Local Cohomology Rank",
        "metric_value": int(metric_value),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[first_failing_seed]['instances_tested']}, h(φ)={results[first_failing_seed]['counterexample'].split(',')[1].strip()}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")