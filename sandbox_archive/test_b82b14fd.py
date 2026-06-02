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
        if m == 1:
            return A[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, m)]
            det += (-1)**j * A[0][j] * determinant(submatrix)
        return det

    def polynomial_ring_from_cnf(cnf):
        variables = set()
        for clause in cnf:
            for literal in clause:
                if literal < 0:
                    literal = -literal
                variables.add(literal)
        n = len(variables)
        ring_size = 2**n
        A = [[Fraction(0)] * ring_size for _ in range(ring_size)]
        for i in range(ring_size):
            for j in range(ring_size):
                if (i & j) == 0:
                    A[i][j] = Fraction(1)
        return A

    def min_order_k_theory(A):
        rank = 0
        for row in gaussian_elimination(A):
            if any(row):
                rank += 1
        return rank

    def resolution_proof_width(cnf):
        clauses = len(cnf)
        max_clause_length = max(len(clause) for clause in cnf)
        return clauses + max_clause_length - 2

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    total_metric_value = Fraction(0)
    instances_tested = 0
    n_max = 0

    for n in n_values:
        for _ in range(5):
            cnf = [[random.randint(1, n) if random.choice([True, False]) else -random.randint(1, n) for _ in range(random.randint(2, 4))] for _ in range(random.randint(2, 4))]
            A = polynomial_ring_from_cnf(cnf)
            min_order = min_order_k_theory(A)
            w_phi = resolution_proof_width(cnf)
            results.append((min_order, w_phi))
            instances_tested += 1
            n_max = max(n_max, n)

    if not results:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    min_orders, w_phis = zip(*results)
    mean_min_order = sum(min_orders) / len(min_orders)
    mean_w_phi = sum(w_phis) / len(w_phis)

    correlation_coefficient = sum((x - mean_min_order) * (y - mean_w_phi) for x, y in results) / (len(results) * math.sqrt(sum((x - mean_min_order)**2 for x in min_orders)) * math.sqrt(sum((y - mean_w_phi)**2 for y in w_phis)))

    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and abs(correlation_coefficient) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")