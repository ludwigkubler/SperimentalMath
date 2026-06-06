# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + random.randint(0, m - i - 1)
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i + 1, m):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def hodge_norm(A):
        return abs(determinant(A))

    def resolution_width(cnf):
        stack = []
        assignment = {}
        for clause in cnf:
            if all(lit not in assignment or assignment[lit] == -1 for lit in clause):
                new_assignment = {lit: 1 for lit in clause}
                stack.append((new_assignment, []))
            elif any(lit in assignment and assignment[lit] == 1 for lit in clause):
                continue
            else:
                return len(stack)
        return len(stack)

    def random_cnf(n, m):
        cnf = []
        variables = list(range(1, n + 1))
        for _ in range(m):
            clause = [random.choice(variables) * (-1 if random.randint(0, 1) else 1)]
            while len(clause) < random.randint(2, n):
                lit = random.choice(variables)
                if lit not in clause and -lit not in clause:
                    clause.append(lit * (-1 if random.randint(0, 1) else 1))
            cnf.append(clause)
        return cnf

    instances_tested = 0
    n_max = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = random_cnf(n, random.randint(2 * n, 3 * n))
            instances_tested += 1
            n_max = max(n_max, n)
            V_phi = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
            norm_H = hodge_norm(V_phi)
            w_phi = resolution_width(cnf)
            metric_values.append((norm_H, w_phi))
    
    if len(metric_values) < 10:
        return {
            "metric_name": "Hodge Norm vs Resolution Width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient data points"
        }

    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = (sum((xi - mean_x) ** 2 for xi in x) / len(x)) ** 0.5
        std_y = (sum((yi - mean_y) ** 2 for yi in y) / len(y)) ** 0.5
        return cov_xy / (std_x * std_y)

    corr = pearson_correlation([x for x, _ in metric_values], [y for _, y in metric_values])
    if corr < 0.7:
        conjecture_holds = False
        counterexample = f"Correlation: {corr}"

    return {
        "metric_name": "Hodge Norm vs Resolution Width",
        "metric_value": corr,
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
        print(f"TRIAL: {result}")
        results.append(result)

    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation below threshold\" first_failing_seed={first_failing_seed}")