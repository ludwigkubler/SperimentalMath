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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(float(A[k][i])))
        A[i], A[max_row] = A[max_row], A[i]
        pivot = float(A[i][i])
        if pivot == 0:
            continue
        for j in range(n):
            A[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = float(A[k][i])
                for j in range(n):
                    A[k][j] -= factor * A[i][j]

def rank(matrix):
    n = len(matrix)
    m = len(matrix[0])
    matrix_copy = [row[:] for row in matrix]
    gaussian_elimination(matrix_copy)
    rank = 0
    for i in range(n):
        if any(abs(matrix_copy[i][j]) > 1e-9 for j in range(m)):
            rank += 1
    return rank

def generate_tseitin_formula(G, d):
    n = len(G)
    variables = {f'x{i}': [] for i in range(n)}
    clauses = []
    
    for v in range(n):
        for u in G[v]:
            if u > v:
                continue
            new_var = f'y{v}_{u}'
            variables[new_var] = []
            clauses.append([new_var, f'~x{v}', f'~x{u}'])
            clauses.append([f'~{new_var}', f'x{v}', f'x{u}'])
    
    for v in range(n):
        new_var = f'y{v}_0'
        variables[new_var] = []
        clauses.append([new_var, f'~x{v}'])
        clauses.append([f'~{new_var}', f'x{v}'])
    
    return variables, clauses

def monotone_circuit_complexity(clauses):
    n = len(clauses)
    complexity = 0
    for clause in clauses:
        complexity += len(clause) - 1
    return complexity

def run_trial(seed: int) -> dict:
    random.seed(seed)
    d = 3
    n_max = 40
    instances_tested = 0
    min_rank_sum = 0
    monotone_complexity_sum = 0
    
    for n in range(5, n_max + 1):
        G = [[j for j in range(n) if (i != j and random.randint(0, d - 1) == 0)] for i in range(n)]
        variables, clauses = generate_tseitin_formula(G, d)
        min_rank = rank(variables)
        monotone_complexity = monotone_circuit_complexity(clauses)
        
        if min_rank <= 0 or monotone_complexity <= 0:
            continue
        
        instances_tested += 1
        min_rank_sum += min_rank
        monotone_complexity_sum += monotone_complexity
    
    if instances_tested == 0:
        return {
            "metric_name": "min_rank",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    min_rank_avg = min_rank_sum / instances_tested
    monotone_complexity_avg = monotone_complexity_sum / instances_tested
    
    correlation_coefficient = (instances_tested * sum(min_rank_avg * monotone_complexity_avg for min_rank_avg, monotone_complexity_avg in zip(range(instances_tested), range(instances_tested))) - 
                               sum(range(instances_tested)) * sum(range(instances_tested))) / math.sqrt(
        instances_tested * sum((min_rank_avg - sum(range(instances_tested)) / instances_tested) ** 2 for min_rank_avg in range(instances_tested)) *
        instances_tested * sum((monotone_complexity_avg - sum(range(instances_tested)) / instances_tested) ** 2 for monotone_complexity_avg in range(instances_tested))
    )
    
    return {
        "metric_name": "min_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": 0.5 <= abs(correlation_coefficient) >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if abs(result["metric_value"]) >= 0.9 or abs(result["metric_value"]) <= -0.9) / len(results)
    
    if all(abs(result["metric_value"]) >= 0.9 or abs(result["metric_value"]) <= -0.9 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(abs(result["metric_value"]) < 0.5 or abs(result["metric_value"]) > 10 for result in results):
        counterexample = next((result for result in results if abs(result["metric_value"]) < 0.5 or abs(result["metric_value"]) > 10), None)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(counterexample)]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")