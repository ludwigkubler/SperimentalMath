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
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below pivot
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(i, n+1):
                if i == k:
                    A[j][k] = 0
                else:
                    A[j][k] += factor * A[i][k]

    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = A[i][-1]
        for j in range(i+1, n):
            x[i] -= A[i][j] * x[j]
        x[i] /= A[i][i]
    
    return x

def matrix_multiplication(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0 for _ in range(k)] for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def norm(matrix):
    n = len(matrix)
    sum_of_squares = 0
    for i in range(n):
        for j in range(n):
            sum_of_squares += matrix[i][j] ** 2
    return math.sqrt(sum_of_squares)

def resolution_width(clauses):
    m, n = len(clauses), len(clauses[0])
    A = [[0 for _ in range(n+1)] for _ in range(m)]
    for i in range(m):
        for j in range(1, n+1):
            if clauses[i][j-1] > 0:
                A[i][clauses[i][j-1]-1] = 1
            else:
                A[i][-1] += abs(clauses[i][j-1])
    
    gaussian_elimination(A)
    width = max(sum(row) for row in A)
    return width

def tseitin_formula(graph):
    n = len(graph)
    clauses = []
    literals = [i+1 for i in range(n)] + [-i-1 for i in range(n)]
    for node in range(n):
        clause = [literals[node]]
        for neighbor in graph[node]:
            clause.append(-literals[neighbor])
        clauses.append(clause)
    
    for literal in literals:
        clause = [-literal]
        for other_literal in literals:
            if abs(literal) != abs(other_literal):
                clause.append(other_literal)
        clauses.append(clause)
    
    return clauses

def geometric_quantization(graph, d):
    n = len(graph)
    A = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if graph[i][j] == 1:
                A[i][j] = 1 / math.sqrt(d)
                A[j][i] = 1 / math.sqrt(d)
    
    return matrix_multiplication(A, A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            graph = [[0] * n for _ in range(n)]
            degree = random.randint(2, min(2*n-2, n-1))
            for i in range(n):
                neighbors = random.sample([j for j in range(n) if j != i], degree)
                for neighbor in neighbors:
                    graph[i][neighbor] = 1
                    graph[neighbor][i] = 1
            
            clauses = tseitin_formula(graph)
            width = resolution_width(clauses)
            
            rho = geometric_quantization(graph, degree)
            norm_rho = norm(rho)
            
            metric_values.append(width / norm_rho)
            instances_tested += 1
            n_max = max(n_max, n)
    
    correlation_coefficient = sum(metric_values[i] * (metric_values[i] - mean) for i in range(len(metric_values))) / (len(metric_values) * std_deviation)
    
    if correlation_coefficient < 0.7:
        conjecture_holds = False
        counterexample = "correlation_coefficient_too_low"
    
    return {
        "metric_name": "resolution_width_over_norm",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean = sum(result["metric_value"] for result in results) / len(results)
    std_deviation = math.sqrt(sum((result["metric_value"] - mean) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_deviation} support_fraction={support_fraction}")
    elif any(result["counterexample"] == "correlation_coefficient_too_low" for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] == "correlation_coefficient_too_low")
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")