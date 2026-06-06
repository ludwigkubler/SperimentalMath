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
    n_values = [5, 10, 15, 20, 30, 40]
    mhr_values = []
    dpll_lengths = []

    for n in n_values:
        cnf = generate_cnf(n)
        matrix = cnf_to_matrix(cnf)
        mhr = minimal_tropical_hermitian_rank(matrix)
        mhr_values.append(mhr)

        proof_length = dpll_proof_length(cnf)
        dpll_lengths.append(proof_length)

    correlation_coefficient = pearson_correlation(mhr_values, dpll_lengths)
    conjecture_holds = abs(correlation_coefficient) >= 0.7

    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Correlation coefficient: {correlation_coefficient}"
    }

def generate_cnf(n):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(n):
        clause = random.sample(variables, 2)
        clauses.append(clause)
    return clauses

def cnf_to_matrix(cnf):
    n = len(cnf)
    matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for i, clause in enumerate(cnf):
        for var in clause:
            matrix[i][var] = 1
    return matrix

def minimal_tropical_hermitian_rank(matrix):
    n = len(matrix)
    rank = 0
    for i in range(n):
        if any(matrix[j][i] == 1 for j in range(n)):
            rank += 1
            for j in range(n):
                if matrix[j][i] == 1:
                    for k in range(n + 1):
                        matrix[j][k] = max(matrix[j][k], matrix[i][k])
    return rank

def dpll_proof_length(cnf):
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if -literal not in c], new_assignment):
                return True
            return False
        pure_literals = [l for l in range(1, len(clauses) + 1) if all(l not in c or -l in c for c in clauses)]
        if pure_literals:
            literal = pure_literals[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if -literal not in c], new_assignment):
                return True
            return False
        literals = [l for l in range(1, len(clauses) + 1)]
        literal = random.choice(literals)
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in clauses if literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in clauses if -literal not in c], new_assignment):
            return True
        return False

    assignment = {}
    return len(cnf) - sum(dpll(clauses, assignment) for _ in range(10))

def pearson_correlation(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
    std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
    std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
    return cov_xy / (std_x * std_y)

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")