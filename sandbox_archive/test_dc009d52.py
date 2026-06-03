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
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B[0]), len(B)
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
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
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def tseitin_formula(n):
        literals = list(range(1, n+1))
        clauses = []
        for i in range(n):
            clauses.append([literals[i]])
        for i in range(n-1):
            for j in range(i+1, n):
                clauses.append([-literals[i], -literals[j]])
                clauses.append([literals[i], literals[j]])
        return literals, clauses

    def symmetric_function(literals, clauses):
        n = len(literals)
        A = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for clause in clauses:
            for literal in clause:
                if literal > 0:
                    i = literal - 1
                    A[i][i] += Fraction(1)
                else:
                    i = -literal - 1
                    A[i][i] -= Fraction(1)
        return A

    def minimal_symplectic_capacity(A):
        det_A = determinant(gaussian_elimination(A))
        if det_A == Fraction(0):
            return Fraction(0)
        return abs(det_A)

    def circuit_monotone_width(A):
        m, n = len(A), len(A[0])
        width = 0
        for i in range(m):
            row_sum = sum(abs(x) for x in A[i])
            if row_sum > width:
                width = row_sum
        return width

    def symmetric_group(n):
        elements = list(range(1, n+1))
        group = []
        def permute(lst, start=0):
            if start == len(lst):
                group.append(lst[:])
                return
            for i in range(start, len(lst)):
                lst[start], lst[i] = lst[i], lst[start]
                permute(lst, start + 1)
                lst[start], lst[i] = lst[i], lst[start]
        permute(elements)
        return group

    def min_symplectic_capacity(A):
        n = len(A)
        capacities = []
        for g in symmetric_group(n):
            B = [[A[g[j]-1][g[k]-1] for k in range(n)] for j in range(n)]
            capacities.append(minimal_symplectic_capacity(B))
        return min(capacities)

    def min_circuit_monotone_width(A):
        n = len(A)
        widths = []
        for g in symmetric_group(n):
            B = [[A[g[j]-1][g[k]-1] for k in range(n)] for j in range(n)]
            widths.append(circuit_monotone_width(B))
        return min(widths)

    def correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x) ** 2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y) ** 2 for i in range(n)) / n
        return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))

    def max_symplectic_capacity(A):
        n = len(A)
        capacities = []
        for g in symmetric_group(n):
            B = [[A[g[j]-1][g[k]-1] for k in range(n)] for j in range(n)]
            capacities.append(minimal_symplectic_capacity(B))
        return max(capacities)

    def max_circuit_monotone_width(A):
        n = len(A)
        widths = []
        for g in symmetric_group(n):
            B = [[A[g[j]-1][g[k]-1] for k in range(n)] for j in range(n)]
            widths.append(circuit_monotone_width(B))
        return max(widths)

    def is_symmetric(A):
        n = len(A)
        for i in range(n):
            for j in range(i+1, n):
                if A[i][j] != A[j][i]:
                    return False
        return True

    def generate_random_polynomial(n):
        coefficients = [random.randint(-10, 10) for _ in range(n+1)]
        return coefficients

    def polynomial_to_matrix(coefficients):
        n = len(coefficients)
        A = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n-i):
                A[i][j] = coefficients[j]
        return A

    def compute_symplectic_capacity_and_width(n):
        literals, clauses = tseitin_formula(n)
        A = symmetric_function(literals, clauses)
        sym_cap = min_symplectic_capacity(A)
        width_mon = min_circuit_monotone_width(A)
        return sym_cap, width_mon

    n_values = [5, 10, 15, 20, 30, 40]
    sym_caps = []
    widths_mon = []

    for n in n_values:
        for _ in range(5):
            coefficients = generate_random_polynomial(n)
            A = polynomial_to_matrix(coefficients)
            if not is_symmetric(A):
                continue
            sym_cap, width_mon = compute_symplectic_capacity_and_width(n)
            sym_caps.append(sym_cap)
            widths_mon.append(width_mon)

    if len(sym_caps) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(sym_caps),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }

    corr = correlation(sym_caps, widths_mon)
    max_sym_cap = max(sym_caps)
    if max_sym_cap > 1.5 * max(widths_mon):
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(sym_caps),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"max_sym_cap={max_sym_cap} > 1.5 * max_widths_mon"
        }

    return {
        "metric_name": "correlation",
        "metric_value": corr,
        "instances_tested": len(sym_caps),
        "n_max": max(n_values),
        "conjecture_holds": corr >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)

    if all("metric_value" not in r or r["metric_value"] is None for r in results):
        print("RESULT: INCONCLUSIVE no_metric_values")
    else:
        valid_results = [r for r in results if "metric_value" in r and r["metric_value"] is not None]
        mean_corr = sum(r["metric_value"] for r in valid_results) / len(valid_results)
        std_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in valid_results) / len(valid_results))
        support_fraction = sum(1 for r in valid_results if r["conjecture_holds"]) / len(valid_results)

        if support_fraction >= 0.95:
            print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")