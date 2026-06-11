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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= factor
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def determinant(matrix):
        rows, cols = len(matrix), len(matrix[0])
        det = 1
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            if max_row != i:
                det *= -1
                matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= factor
            for k in range(i + 1, rows):
                factor = matrix[k][i]
                for j in range(cols):
                    matrix[k][j] -= factor * matrix[i][j]
        return det

    def construct_quandle(cnf):
        literals = set()
        for clause in cnf:
            for lit in clause:
                literals.add(abs(lit))
        quandle_size = len(literals)
        truth_table = {}
        for a in range(quandle_size):
            for b in range(quandle_size):
                assignment = {l: (a + 1) % quandle_size if l == i else (b + 1) % quandle_size for i, l in enumerate(literals)}
                sat = True
                for clause in cnf:
                    if all(assignment[lit] != 0 for lit in clause):
                        sat = False
                        break
                truth_table[(a, b)] = int(sat)
        quandle_operation = [[truth_table[(a, b)] for b in range(quandle_size)] for a in range(quandle_size)]
        return quandle_operation

    def dpll(cnf):
        if not cnf:
            return True
        unit_clauses = [c[0] for c in cnf if len(c) == 1]
        if unit_clauses:
            lit = unit_clauses[0]
            new_cnf = [[l for l in c if l != -lit and l != lit] for c in cnf]
            return dpll(new_cnf)
        pure_literals = {}
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    if lit not in pure_literals:
                        pure_literals[lit] = True
                    elif not pure_literals[lit]:
                        pure_literals[lit] = False
                else:
                    if -lit not in pure_literals:
                        pure_literals[-lit] = False
                    elif pure_literals[-lit]:
                        pure_literals[-lit] = True
        for lit, polarity in pure_literals.items():
            new_cnf = [[l for l in c if l != -lit and l != lit] for c in cnf]
            if dpll(new_cnf):
                return True
        return False

    def generate_random_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(random.randint(1, n))]
            if all(lit not in [-l for l in clause] for lit in clause):
                clauses.append(clause)
        return clauses

    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y))
        return cov_xy / (std_x * std_y)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    total_instances = 0
    max_n = 0

    for n in n_values:
        for _ in range(5):
            cnf = generate_random_cnf(n)
            total_instances += len(cnf)
            max_n = max(max_n, n)
            quandle_operation = construct_quandle(cnf)
            dpll_width = dpll(cnf)
            minimal_order = determinant(quandle_operation)
            results.append((minimal_order, dpll_width))

    if not results:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    x, y = zip(*results)
    correlation_coefficient = pearson_correlation(x, y)

    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": total_instances,
        "n_max": max_n,
        "conjecture_holds": correlation_coefficient >= 0.5 and abs(sum(y) / len(y)) <= 10 * min(x),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if not results:
        print("RESULT: INCONCLUSIVE reason=empty_results")
    else:
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        elif any(not r["conjecture_holds"] for r in results):
            first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_support")