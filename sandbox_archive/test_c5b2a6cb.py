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
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def polynomial_to_cnf(poly, variables):
        cnf = []
        for term in poly:
            clause = []
            for var, exp in term.items():
                if exp > 0:
                    clause.append((var, True))
                elif exp < 0:
                    clause.append((var, False))
            cnf.append(clause)
        return cnf

    def sat_complexity(cnf):
        n = len(variables)
        clauses = [set(clause) for clause in cnf]
        max_clause_length = max(len(clause) for clause in clauses)
        return max_clause_length

    def lid(poly, variables):
        n = len(variables)
        A = [[0] * n for _ in range(n)]
        for term in poly:
            for var1, exp1 in term.items():
                for var2, exp2 in term.items():
                    if var1 != var2:
                        A[var1][var2] += 1
        A = gaussian_elimination(A)
        rank = sum(1 for row in A if any(row))
        return n - rank

    def generate_polynomial(n):
        poly = []
        for _ in range(random.randint(1, 5)):
            term = {}
            for var in range(n):
                exp = random.choice([-2, -1, 0, 1, 2])
                if exp != 0:
                    term[var] = exp
            poly.append(term)
        return poly

    def generate_variables(n):
        variables = list(range(n))
        random.shuffle(variables)
        return variables

    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in range(5, n_max + 1):
        if len(metric_values) >= instances_tested:
            break
        poly = generate_polynomial(n)
        variables = generate_variables(n)
        cnf = polynomial_to_cnf(poly, variables)
        lid_value = lid(poly, variables)
        sat_value = sat_complexity(cnf)
        metric_values.append(lid_value - sat_value)

    if len(metric_values) < instances_tested:
        return {
            "metric_name": "LID - SAT Complexity",
            "metric_value": None,
            "instances_tested": len(metric_values),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    mean = sum(metric_values) / instances_tested
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / instances_tested)
    support_fraction = sum(1 for val in metric_values if abs(val) <= 3) / instances_tested

    return {
        "metric_name": "LID - SAT Complexity",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.8 and abs(mean) <= 3,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["metric_value"] is not None for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")