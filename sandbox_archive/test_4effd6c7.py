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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for k in range(n):
                if k != i:
                    factor = Fraction(A[k][i])
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return [b[i][0] for i in range(n)]

    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def matrix_inverse(A, mod):
        n = len(A)
        I = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
        A_inv = []
        for row in A:
            A_inv.append([x % mod for x in row])
        for i in range(n):
            factor = Fraction(A_inv[i][i], 1)
            for j in range(n):
                A_inv[i][j] /= factor
                I[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = Fraction(A_inv[k][i], 1)
                    for j in range(n):
                        A_inv[k][j] -= factor * A_inv[i][j]
                        I[k][j] -= factor * I[i][j]
        return [[int(x) for x in row] for row in I]

    def dpll_search_tree_width(formula):
        n = len(formula)
        stack = []
        width = 0
        for i in range(n):
            if formula[i] == '1':
                stack.append(i)
                width += 1
            elif formula[i] == '0':
                while stack and stack[-1] != i - 1:
                    stack.pop()
                    width -= 1
                if stack:
                    stack.pop()
        return width

    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n + 1)]
        clauses = []
        for i in range(1, n + 1):
            clauses.append(f'{variables[i-1]}')
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                clauses.append(f'~{variables[i-1]} | ~{variables[j-1]}')
        return ' & '.join(clauses)

    def eta_invariant(modular_form):
        # Placeholder function to compute the Eta-invariant
        # This is a dummy implementation and should be replaced with actual computation
        return random.random()

    instances_tested = 0
    n_max = 40
    eta_values = []
    width_values = []

    for n in range(5, 41):
        formula = tseitin_formula(n)
        # Placeholder for modular form computation
        modular_form = [random.randint(0, 1) for _ in range(n)]
        eta = eta_invariant(modular_form)
        width = dpll_search_tree_width(formula)
        eta_values.append(eta)
        width_values.append(width)
        instances_tested += 1

    if not eta_values or not width_values:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }

    mean_eta = sum(eta_values) / len(eta_values)
    mean_width = sum(width_values) / len(width_values)

    numerator = sum((eta - mean_eta) * (width - mean_width) for eta, width in zip(eta_values, width_values))
    denominator = math.sqrt(sum((eta - mean_eta)**2 for eta in eta_values)) * math.sqrt(sum((width - mean_width)**2 for width in width_values))

    if denominator == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "denominator_zero"
        }

    correlation_coefficient = numerator / denominator

    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results if result["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")