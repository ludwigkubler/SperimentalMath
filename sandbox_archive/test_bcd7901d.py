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
    
    def generate_cnf(n, c):
        clauses = []
        for _ in range(c):
            clause = set(random.sample(range(1, n+1), 3))
            while len(clause) < 3:
                clause.add(random.randint(1, n))
            clauses.append(clause)
        return clauses

    def adjacency_matrix(n, clauses):
        A = [[0] * n for _ in range(n)]
        for clause in clauses:
            for i in clause:
                for j in clause:
                    if i != j:
                        A[i-1][j-1] += 1
        return A

    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            max_row = None
            for r in range(i, m):
                if A[r][i] != 0:
                    max_row = r
                    break
            if max_row is None:
                continue
            A[i], A[max_row] = A[max_row], A[i]
            rank += 1
            for r in range(m):
                if r != i and A[r][i] != 0:
                    factor = Fraction(A[r][i], A[i][i])
                    for c in range(n):
                        A[r][c] -= factor * A[i][c]
        return rank

    def geometric_entropy(A):
        n = len(A)
        rank = gaussian_elimination(A)
        return math.log2(n) - math.log2(rank)

    def correlation_coefficient(x, y):
        n = len(x)
        if n < 2:
            return None
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        if std_x == 0 or std_y == 0:
            return None
        return cov / (std_x * std_y)

    n_values = [5, 10, 15, 20, 30, 40]
    H_min_values = []
    c_values = []

    for n in n_values:
        for _ in range(5):
            clauses = generate_cnf(n, random.randint(1, n))
            A = adjacency_matrix(n, clauses)
            H_min = geometric_entropy(A)
            if H_min is not None:
                H_min_values.append(H_min)
                c_values.append(len(clauses))

    r = correlation_coefficient(H_min_values, c_values)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": r,
        "instances_tested": len(H_min_values),
        "n_max": max(n_values),
        "conjecture_holds": r is not None and abs(r) >= 0.9,
        "counterexample": "" if r is not None else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_r = sum(r["metric_value"] for r in results) / len(results)
    std_r = math.sqrt(sum((r["metric_value"] - mean_r) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")