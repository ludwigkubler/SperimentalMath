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
        C = [[0 for _ in range(p)] for _ in range(m)]
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

    def is_symplectic(A):
        n = len(A)
        if n % 2 != 0:
            return False
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        J = [[0 if i == j or (i + j) % 2 == 0 else 1 for j in range(n)] for i in range(n)]
        return matrix_multiplication(matrix_multiplication(A, I), A) == J and determinant(A) != 0

    def generate_cnf(n):
        clauses = []
        for _ in range(2**n - n - 1):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(random.randint(1, n))]
            if all(clause[i] != -clause[j] for i in range(len(clause)) for j in range(i+1, len(clause))):
                clauses.append(clause)
        return clauses

    def resolution_width(cnf):
        queue = cnf[:]
        learned_clauses = []
        while True:
            new_clause = None
            for clause1 in queue:
                for clause2 in queue:
                    if set(clause1) & set(clause2):
                        new_clause = [l for l in clause1 + clause2 if l not in set(clause1) & set(clause2)]
                        if len(new_clause) == 0:
                            return len(learned_clauses)
                        learned_clauses.append(new_clause)
            if new_clause is None:
                break
            queue.append(new_clause)
        return len(learned_clauses)

    def symplectic_leaves(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        A = [[0] * (2*n) for _ in range(2*n)]
        for i, clause in enumerate(cnf):
            for lit in clause:
                if lit > 0:
                    A[i][lit-1] = 1
                else:
                    A[i][n-lit] = -1
        rank = 0
        for row in gaussian_elimination(A):
            if any(row[j] != 0 for j in range(2*n)):
                rank += 1
        return rank

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        instances_tested = len(cnf)
        symplectic_leaves_count = symplectic_leaves(cnf)
        resolution_width_value = resolution_width(cnf)
        if symplectic_leaves_count > 3 * resolution_width_value:
            counterexample = f"n={n}, symplectic_leaves={symplectic_leaves_count}, resolution_width={resolution_width_value}"
            conjecture_holds = False
        else:
            counterexample = ""
            conjecture_holds = True
        results.append({
            "metric_name": "symplectic_leaves_bound",
            "metric_value": symplectic_leaves_count,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })

    return {
        "seed": seed,
        **results[0],
        "mean_metric_value": sum(result["metric_value"] for result in results) / len(results),
        "std_metric_value": math.sqrt(sum((result["metric_value"] - results[0]["mean_metric_value"])**2 for result in results) / len(results)),
        "support_fraction": sum(1 for result in results if result["conjecture_holds"]) / len(results)
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["mean_metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["mean_metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.8) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"symplectic_leaves > 3 * resolution_width\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")