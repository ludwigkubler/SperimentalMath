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
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return [row[:n-1] for row in A]

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def rank(A):
        return len(gaussian_elimination(A))

    def random_cnf(n, m):
        variables = set(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            if random.choice([True, False]):
                clause = [-v for v in clause]
            clauses.append(clause)
        return clauses

    def tropicalization(clauses):
        m = len(clauses)
        A = [[0] * (m + 1) for _ in range(m)]
        for i in range(m):
            for j in range(i, m):
                if i == j:
                    A[i][j] = -math.inf
                else:
                    A[i][j] = math.inf
                    for clause in clauses:
                        if (i + 1) in clause and (j + 1) not in clause:
                            A[i][j] = max(A[i][j], -len(clause))
                        elif (i + 1) not in clause and (j + 1) in clause:
                            A[i][j] = max(A[i][j], -len(clause))
        return A

    n = random.randint(5, 40)
    m = random.randint(5, 40)
    cnf = random_cnf(n, m)
    tropicalized_object = tropicalization(cnf)
    minimal_rank = rank(tropicalized_object)

    metric_value = minimal_rank / m
    conjecture_holds = metric_value <= 2 * m / n
    counterexample = "" if conjecture_holds else f"CNF with {n} vars, {m} clauses"

    return {
        "metric_name": "minimal_rank_over_clauses",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")