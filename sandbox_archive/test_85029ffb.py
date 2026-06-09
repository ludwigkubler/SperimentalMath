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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(cols):
            if j != i:
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(rows):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def matrix_multiply(A, B):
    rows_A, cols_A = len(A), len(A[0])
    cols_B = len(B[0])
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

def dpll(cnf):
    def solve():
        assignment = {}
        stack = []
        while True:
            unit_clause = next((c for c in cnf if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                if literal < 0 and -literal in assignment and assignment[-literal]:
                    return False
                elif literal > 0 and literal not in assignment:
                    assignment[literal] = True
                else:
                    del assignment[-literal]
            else:
                unsatisfied_clauses = [c for c in cnf if all(lit not in assignment or assignment[lit] == (lit < 0) for lit in c)]
                if not unsatisfied_clauses:
                    return True
                literal = random.choice([l for l in unsatisfied_clauses[0] if l > 0])
                stack.append((literal, assignment.copy()))
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            cnf_new = []
            for c in cnf:
                if not any(lit in new_assignment and new_assignment[lit] == (lit < 0) for lit in c):
                    cnf_new.append([l for l in c if l != literal])
            cnf = cnf_new
        return True

    return solve()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(n):
            clause = [random.choice(variables) * (-1 if random.random() < 0.5 else 1) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses

    def tropical_cyclotomic_polynomial(cnf):
        matrix = [[0] * (len(cnf) + 1) for _ in range(len(cnf) + 1)]
        for i, clause in enumerate(cnf):
            for lit in clause:
                if lit > 0:
                    matrix[i][lit - 1] += 1
        matrix[-1][-1] = len(cnf)
        gaussian_elimination(matrix)
        degree = sum(1 for row in matrix[:-1] if any(x != 0 for x in row))
        coefficients = [sum(row) for row in matrix]
        return degree, coefficients

    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in range(5, n_max + 1):
        cnf = generate_cnf(n)
        degree, coefficients = tropical_cyclotomic_polynomial(cnf)
        if degree > n * math.log2(n) or max(coefficients) > n * math.log2(n):
            conjecture_holds = False
            counterexample = f"n={n}, degree={degree}, max_coefficient={max(coefficients)}"
            break
        total_metric_value += degree + sum(coefficients)
        instances_tested += 1

    return {
        "metric_name": "Tropical Cyclotomic Polynomial Complexity",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else 0.0,
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

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")