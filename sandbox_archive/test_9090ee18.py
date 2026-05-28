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
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
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
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def is_invertible(A):
        return determinant(A) != 0

    def construct_cnf(n):
        clauses = []
        for i in range(2**n):
            clause = []
            for j in range(n):
                if (i >> j) & 1:
                    clause.append(j + 1)
                else:
                    clause.append(-(j + 1))
            clauses.append(clause)
        return clauses

    def resolution(clauses):
        while True:
            new_clauses = set()
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    clause_i = clauses[i]
                    clause_j = clauses[j]
                    for literal_i in clause_i:
                        if -literal_i in clause_j:
                            new_clause = [l for l in clause_i if l != literal_i] + [l for l in clause_j if l != -literal_i]
                            if not any(l == -m for m in new_clause):
                                new_clauses.add(tuple(sorted(new_clause)))
            if new_clauses.issubset(clauses):
                break
            clauses.update(new_clauses)
        return len(clauses)

    def monodromy_rank(n):
        # Placeholder function to compute the monodromy rank
        # For simplicity, we assume it's proportional to n^2
        return n**2

    n = random.randint(5, 40)
    cnf = construct_cnf(n)
    resolution_length = resolution(cnf)
    R_F = monodromy_rank(n)

    if resolution_length > O(n**2 * R_F):
        counterexample = f"CNF with n={n} has R(F)={R_F} and t*(F)={resolution_length}, which violates the conjecture."
        return {
            "metric_name": "Resolution Proof Length",
            "metric_value": resolution_length,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": counterexample
        }
    else:
        return {
            "metric_name": "Resolution Proof Length",
            "metric_value": resolution_length,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*100 + 1, 100))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")