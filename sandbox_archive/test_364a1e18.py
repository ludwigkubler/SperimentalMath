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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def construct_metric_space(clauses, variables):
    n = len(variables)
    M = [[0] * n for _ in range(n)]
    for clause in clauses:
        for i in range(len(clause)):
            for j in range(i + 1, len(clause)):
                var1, sign1 = clause[i]
                var2, sign2 = clause[j]
                if var1 == var2 and sign1 != sign2:
                    M[variables.index(var1)][variables.index(var2)] += 1
    return M

def calculate_geometric_entropy(M):
    n = len(M)
    total = sum(sum(row) for row in M)
    entropy = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            if M[i][j] > 0:
                p = Fraction(M[i][j], total)
                entropy += -p * math.log2(p)
    return entropy

def dpll(clauses, assignment):
    if not clauses:
        return True
    unit_clauses = [c for c in clauses if len(c) == 1]
    if unit_clauses:
        var, sign = unit_clauses[0][0]
        if (var, sign) in assignment or (-var, -sign) in assignment:
            return False
        assignment[var] = sign
        return dpll([c for c in clauses if not any(v == var and s == sign for v, s in c)], assignment)
    pure_literals = [v for v in variables if all(v != x or (x, s) not in assignment for x, s in clause) for clause in clauses]
    if pure_literals:
        var = pure_literals[0]
        return dpll([c for c in clauses if not any(v == var and s == sign for v, s in c)], {**assignment, var: 1})
    var = random.choice(variables)
    assignment[var] = 1
    if dpll(clauses, assignment):
        return True
    del assignment[var]
    assignment[-var] = -1
    return dpll(clauses, assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    variables = [f'x{i+1}' for i in range(30)]
    n_max = 40
    instances_tested = 0
    metric_values = []
    
    for n in {5, 10, 15, 20, 30, 40}:
        for _ in range(5):
            clauses = []
            for _ in range(n):
                clause = [(random.choice(variables), random.choice([1, -1]))]
                while len(clause) < n // 2 + 1:
                    var = random.choice(variables)
                    if (var, 1) not in clause and (-var, -1) not in clause:
                        clause.append((var, random.choice([1, -1])))
                clauses.append(clause)
            M = construct_metric_space(clauses, variables)
            het_M = calculate_geometric_entropy(M)
            d_phi = 0
            for _ in range(3):
                assignment = {}
                if dpll(clauses, assignment):
                    d_phi += len(assignment)
            instances_tested += 1
            metric_values.append((het_M, d_phi))
    
    correlation_coefficient = 0.0
    if len(metric_values) > 1:
        het_values = [x[0] for x in metric_values]
        d_phi_values = [x[1] for x in metric_values]
        mean_het = sum(het_values) / len(het_values)
        mean_d_phi = sum(d_phi_values) / len(d_phi_values)
        numerator = sum((het - mean_het) * (d_phi - mean_d_phi) for het, d_phi in metric_values)
        denominator = math.sqrt(sum((het - mean_het) ** 2 for het in het_values)) * math.sqrt(sum((d_phi - mean_d_phi) ** 2 for d_phi in d_phi_values))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")