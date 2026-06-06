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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses

    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        literal = next((lit for lit in range(1, len(cnf) + 1) if lit not in assignment and -lit not in assignment), None)
        if literal is None:
            return False
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        new_assignment[-literal] = True
        return dpll([c for c in cnf if -literal not in c and literal not in c], new_assignment)

    def hermitian_rank(matrix):
        n = len(matrix)
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                M[i][j] = max(abs(matrix[i][k]) + abs(matrix[j][k]) for k in range(n))
        rank = 0
        for i in range(n):
            if all(M[j][i] == 0 for j in range(rank)):
                continue
            for j in range(rank, n):
                M[j][i], M[i][j] = M[i][j], M[j][i]
            rank += 1
            for j in range(i + 1, n):
                factor = M[j][i] / M[i][i]
                for k in range(n):
                    M[j][k] -= factor * M[i][k]
        return rank

    def matrix_from_cnf(cnf):
        n = len(cnf)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    matrix[lit - 1][lit] += 1
                else:
                    matrix[-lit - 1][-lit] += 1
        return matrix

    n_max = 40
    instances_tested = 30
    mhr_values = []
    dpll_lengths = []

    for _ in range(instances_tested):
        cnf = generate_cnf(n_max)
        matrix = matrix_from_cnf(cnf)
        mhr_value = hermitian_rank(matrix)
        dpll_length = dpll(cnf)
        if dpll_length:
            mhr_values.append(mhr_value)
            dpll_lengths.append(dpll_length)

    if not mhr_values or not dpll_lengths:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_range_in_randrange"
        }

    mean_mhr = sum(mhr_values) / len(mhr_values)
    mean_dpll = sum(dpll_lengths) / len(dpll_lengths)
    covariance = sum((m - mean_mhr) * (d - mean_dpll) for m, d in zip(mhr_values, dpll_lengths)) / len(mhr_values)
    variance_mhr = sum((m - mean_mhr) ** 2 for m in mhr_values) / len(mhr_values)
    variance_dpll = sum((d - mean_dpll) ** 2 for d in dpll_lengths) / len(dpll_lengths)
    correlation_coefficient = covariance / math.sqrt(variance_mhr * variance_dpll)

    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": abs(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={r['seed']}")
                break