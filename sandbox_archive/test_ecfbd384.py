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

def generate_cnf(n):
    num_clauses = n * (n + 1) // 2
    cnf = []
    for _ in range(num_clauses):
        clause = [random.randint(-1, -num_vars), random.randint(1, num_vars)]
        if len(set(clause)) == 2:
            cnf.append(clause)
    return cnf

def power_iteration(matrix, n, max_iter=1000):
    v = [1.0] * n
    for _ in range(max_iter):
        v = matrix @ v
        norm = sum(x**2 for x in v) ** 0.5
        if norm == 0:
            break
        v = [x / norm for x in v]
    return v

def laplacian_matrix(cnf, n):
    degree = [0] * (n + 1)
    adjacency = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in cnf:
        for lit in clause:
            if lit > 0:
                degree[lit] += 1
            else:
                degree[-lit] += 1
    for clause in cnf:
        for i, lit1 in enumerate(clause):
            for j, lit2 in enumerate(clause):
                if i < j and (lit1 == -lit2 or lit2 == -lit1):
                    adjacency[lit1][lit2] = 1
                    adjacency[lit2][lit1] = 1
    laplacian = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        laplacian[i][i] = degree[i]
        for j in range(i + 1, n + 1):
            laplacian[i][j] = -adjacency[i][j]
            laplacian[j][i] = -adjacency[j][i]
    return laplacian

def second_smallest_eigenvalue(laplacian, n):
    eigenvalues = []
    for _ in range(10):  # Compute a few eigenvalues
        v = power_iteration(laplacian, n)
        lambda_val = sum(x * y for x, y in zip(v, laplacian @ v)) / sum(x**2 for x in v)
        eigenvalues.append(lambda_val)
    sorted_eigenvalues = sorted(eigenvalues)
    return sorted_eigenvalues[1]

def resolution_width(cnf):
    # Simplified DPLL solver to estimate width
    stack = []
    assignment = {}
    def dpll():
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            lit = unit_clause[0]
            assignment[lit] = True
            cnf.remove(unit_clause)
            for clause in cnf:
                if lit in clause:
                    clause.remove(lit)
                elif -lit in clause:
                    return False
            if dpll():
                return True
            del assignment[lit]
            cnf.append(unit_clause)
        else:
            literal = next((i for i in range(1, n + 1) if i not in assignment and -i not in assignment), None)
            assignment[literal] = True
            stack.append(literal)
            if dpll():
                return True
            del assignment[literal]
            stack.pop()
            assignment[-literal] = True
            for clause in cnf:
                if literal in clause:
                    clause.remove(literal)
                elif -literal in clause:
                    return False
            if dpll():
                return True
            del assignment[-literal]
        return False
    width = 0
    while not dpll():
        width += 1
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Sample 5 instances per size
            cnf = generate_cnf(n)
            laplacian = laplacian_matrix(cnf, n)
            eig2 = second_smallest_eigenvalue(laplacian, n)
            width = resolution_width(cnf)
            if eig2 == 0:
                continue
            metric_values.append(eig2 / width)
            instances_tested += 1

    mean_value = sum(metric_values) / len(metric_values)
    std_value = (sum((x - mean_value)**2 for x in metric_values) / len(metric_values))**0.5
    correlation_coefficient = sum((x - mean_value) * (y - mean_value) for x, y in zip(metric_values, range(1, instances_tested + 1))) / (len(metric_values) * std_value)
    
    if correlation_coefficient < 0.7:
        conjecture_holds = False
        counterexample = f"Correlation coefficient {correlation_coefficient} is less than 0.7"

    return {
        "metric_name": "eig2 / width",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_less_than_0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")