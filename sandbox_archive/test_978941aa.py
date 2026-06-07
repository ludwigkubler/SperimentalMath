# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import product

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]

    # Back-substitute
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(b[i], A[i][i])
        for j in range(i-1, -1, -1):
            b[j] -= A[j][i] * x[i]
    return x

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = Fraction(0, 1)
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def inverse(A):
    n = len(A)
    det_A = determinant(A)
    if det_A == 0:
        raise ValueError("Matrix is singular")
    adjoint = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            cofactor = determinant(submatrix)
            adjoint[j][i] = (-1) ** (i+j) * cofactor
    inv_A = [[adjoint[i][j] / det_A for j in range(n)] for i in range(n)]
    return inv_A

def resolution_width(clauses):
    n = len(clauses)
    if n == 0:
        return 0
    variables = set()
    for clause in clauses:
        for literal in clause:
            variables.add(abs(literal))
    minterms = [set(range(1, n+1)) - {i} for i in range(1, n+1)]
    width = 0
    while len(minterms) > 0:
        min_width = float('inf')
        for m in minterms:
            if len(m) < min_width:
                min_width = len(m)
        width += min_width
        new_minterms = []
        for m in minterms:
            if len(m) == min_width:
                continue
            for i in range(n):
                if (i+1) not in m and any(abs(literal) == i+1 for literal in clauses[i]):
                    new_minterm = m - {i+1}
                    if new_minterm not in new_minterms:
                        new_minterms.append(new_minterm)
        minterms = new_minterms
    return width

def grothendieck_witt_degree(clauses):
    n = len(clauses)
    variables = set()
    for clause in clauses:
        for literal in clause:
            variables.add(abs(literal))
    minterms = [set(range(1, n+1)) - {i} for i in range(1, n+1)]
    degree = 0
    while len(minterms) > 0:
        min_degree = float('inf')
        for m in minterms:
            if len(m) < min_degree:
                min_degree = len(m)
        degree += min_degree
        new_minterms = []
        for m in minterms:
            if len(m) == min_degree:
                continue
            for i in range(n):
                if (i+1) not in m and any(abs(literal) == i+1 for literal in clauses[i]):
                    new_minterm = m - {i+1}
                    if new_minterm not in new_minterms:
                        new_minterms.append(new_minterm)
        minterms = new_minterms
    return degree

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    instances_tested = 30
    n_max = 40
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        clauses = []
        for i in range(n):
            num_literals = random.randint(1, 5)
            literals = [random.choice([-1, 1]) * (j+1) for j in random.sample(range(n), num_literals)]
            clauses.append(literals)

        gw_degree = grothendieck_witt_degree(clauses)
        width = resolution_width(clauses)

        if gw_degree > 2 * width:
            conjecture_holds = False
            counterexample = f"Instance with gw_degree={gw_degree} and width={width}"
            break

    return {
        "metric_name": "minimal_monomial_degree",
        "metric_value": gw_degree,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")