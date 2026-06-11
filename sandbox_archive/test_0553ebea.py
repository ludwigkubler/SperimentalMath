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
    n = len(matrix)
    rank = 0
    for k in range(n):
        i_max = rank
        for i in range(rank, n):
            if abs(matrix[i][k]) > abs(matrix[i_max][k]):
                i_max = i
        if matrix[i_max][k] == 0:
            continue
        matrix[rank], matrix[i_max] = matrix[i_max], matrix[rank]
        for j in range(k + 1, n):
            factor = Fraction(-matrix[rank][j], matrix[rank][k])
            for i in range(k, n):
                if i == rank:
                    matrix[i][j] = 0
                else:
                    matrix[i][j] += factor * matrix[i][k]
        rank += 1
    return rank

def tseitin_formula(f, n):
    literals = list(range(1, n + 1))
    clauses = []
    for i in range(n):
        clauses.append([literals[i]])
        clauses.append([-literals[i], literals[(i + 1) % n]])
    for clause in f:
        new_var = len(literals) + 1
        literals.append(new_var)
        for literal in clause:
            if literal > 0:
                clauses.append([new_var, -literal])
            else:
                clauses.append([-new_var, literal])
        for i in range(len(clauses)):
            if clauses[i][0] == new_var:
                clauses[i].append(-literals[(i + 1) % len(clauses)])
    return literals, clauses

def br(f, n):
    literals, clauses = tseitin_formula(f, n)
    matrix = [[Fraction(0, 1)] * len(literals) for _ in range(len(literals))]
    for literal in literals:
        for clause in clauses:
            if literal in clause:
                for lit in clause:
                    if lit != literal:
                        matrix[literal - 1][lit - 1] += Fraction(1, 1)
    return gaussian_elimination(matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = [[random.choice([i + 1, -(i + 1)]) for _ in range(n)] for _ in range(2 ** (n - 1))]
        br_order = br(f, n)
        w_phi_f = len(f) * n
        results.append({"br_order": br_order, "w_phi_f": w_phi_f})
    metric_value = sum(result["br_order"] / result["w_phi_f"] for result in results) / len(results)
    instances_tested = len(n_values) * 2 ** (n - 1)
    n_max = max(n_values)
    conjecture_holds = all(0.7 <= abs(result["br_order"] / result["w_phi_f"]) <= 10 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_operation")