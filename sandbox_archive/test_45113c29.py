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
            for j in range(n):
                if j != i:
                    factor = Fraction(A[j][i], A[i][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C

    def hodge_polynomial(A):
        n = len(A)
        if n == 0:
            return 1
        det = Fraction(1)
        for i in range(n):
            det *= A[i][i]
        return det

    def resolution_width(phi):
        # Simplified DPLL solver to estimate width
        clauses = phi.split(' ')
        literals = set()
        for clause in clauses:
            literals.update(clause.split())
        return len(literals)

    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = random.sample(range(1, n + 1), 2)
            cnf.append(f"{random.choice([str(x) for x in clause])} {random.choice([str(-x) for x in clause])}")
        return ' '.join(cnf)

    def projective_variety(phi):
        # Simplified encoding of the projective variety
        n = len(phi.split(' '))
        A = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            A[i][i] = Fraction(1)
        return gaussian_elimination(A)

    def correlation(X, Y):
        mean_X = sum(X) / len(X)
        mean_Y = sum(Y) / len(Y)
        cov = sum((X[i] - mean_X) * (Y[i] - mean_Y) for i in range(len(X))) / len(X)
        std_X = math.sqrt(sum((X[i] - mean_X) ** 2 for i in range(len(X))) / len(X))
        std_Y = math.sqrt(sum((Y[i] - mean_Y) ** 2 for i in range(len(Y))) / len(Y))
        return cov / (std_X * std_Y)

    n_values = [5, 10, 15, 20, 30, 40]
    X, Y = [], []
    instances_tested = 0
    n_max = 0

    for n in n_values:
        for _ in range(5):
            phi = generate_cnf(n, random.randint(1, n * 2))
            A = projective_variety(phi)
            deg_H = hodge_polynomial(A)
            w_phi = resolution_width(phi)
            X.append(deg_H)
            Y.append(w_phi)
            instances_tested += 1
            if n > n_max:
                n_max = n

    corr_coeff = correlation(X, Y)
    conjecture_holds = corr_coeff >= 0.7
    counterexample = "" if conjecture_holds else f"Correlation coefficient {corr_coeff} < 0.7"

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": corr_coeff,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={math.sqrt(sum((r['metric_value'] - mean_corr_coeff) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")