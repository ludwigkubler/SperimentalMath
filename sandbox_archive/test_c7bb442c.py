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
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def rank(A):
        return sum(1 for row in gaussian_elimination(A) if any(row))

    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
            while len(set(clause)) != len(clause):
                clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses

    def resolution_width(cnf):
        queue = cnf[:]
        visited = set()
        width = 0
        while queue:
            literal = queue.pop()
            if literal in visited:
                continue
            visited.add(literal)
            for clause in cnf:
                if literal in clause:
                    new_clause = [l for l in clause if l != literal and -l not in clause]
                    if len(new_clause) == 0:
                        return width
                    queue.append(-new_clause[0])
            width += 1
        return width

    n_max = 40
    instances_tested = 0
    mrank_sum = 0
    w_sum = 0
    mrank_squared_sum = 0
    w_squared_sum = 0
    mw_product_sum = 0

    for n in range(5, 41):
        for _ in range(30):
            cnf = generate_cnf(n, random.randint(1, n**2))
            mrank = rank([[sum(abs(l) for l in clause if l > 0) for clause in cnf]])
            w = resolution_width(cnf)
            instances_tested += 1
            mrank_sum += mrank
            w_sum += w
            mrank_squared_sum += mrank ** 2
            w_squared_sum += w ** 2
            mw_product_sum += mrank * w

    n = instances_tested
    mean_mrank = mrank_sum / n
    mean_w = w_sum / n
    variance_mrank = (mrank_squared_sum / n) - (mean_mrank ** 2)
    variance_w = (w_squared_sum / n) - (mean_w ** 2)
    covariance = (mw_product_sum / n) - (mean_mrank * mean_w)

    correlation_coefficient = covariance / math.sqrt(variance_mrank * variance_w)
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else f"correlation_coefficient={correlation_coefficient}"

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and min(r["metric_value"] for r in results if not r["conjecture_holds"]) >= 0.5:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient<0.8' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_evidence")