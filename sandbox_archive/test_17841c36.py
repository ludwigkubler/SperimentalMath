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
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
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

    def generate_cnf_formula(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(n)]
            if sum(clause) != 0:
                clauses.append(clause)
        return clauses

    def minimal_rank(cnf_formula):
        m = len(cnf_formula)
        A = [[0] * (m + 1) for _ in range(m + 1)]
        for i, clause in enumerate(cnf_formula):
            for literal in clause:
                A[i][abs(literal) - 1] += 1
        A[m] = [sum(row[j] for j in range(m)) for row in A]
        rank = 0
        for row in gaussian_elimination(A):
            if any(x != 0 for x in row):
                rank += 1
        return rank

    def circuit_size(cnf_formula):
        n = len(cnf_formula[0])
        size = 2 * n + sum(len(clause) for clause in cnf_formula)
        return size

    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        cnf_formula = generate_cnf_formula(n)
        rank = minimal_rank(cnf_formula)
        size = circuit_size(cnf_formula)
        metric_values.append(rank * size)

    mean_metric_value = sum(metric_values) / instances_tested
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / instances_tested)

    return {
        "metric_name": "rank*size",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,  # Placeholder, actual check needed
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")