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
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        pivot = matrix[i][i]
        if pivot == 0:
            continue
        for j in range(i, n):
            matrix[i][j] /= pivot
        for j in range(n):
            if j != i and matrix[j][i] != 0:
                factor = matrix[j][i]
                for k in range(i, n):
                    matrix[j][k] -= factor * matrix[i][k]

def matrix_multiplication(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def tseitin_formula(circuit):
    n = len(circuit)
    literals = [f"x{i+1}" for i in range(n)]
    clauses = []
    for i, gate in enumerate(circuit):
        if gate[0] == 'AND':
            a, b = gate[1], gate[2]
            literals[i] = f"y{i+1}"
            clauses.append([literals[a-1], literals[b-1], f"~{literals[i]}"])
        elif gate[0] == 'OR':
            a, b = gate[1], gate[2]
            literals[i] = f"y{i+1}"
            clauses.append([f"~{literals[a-1]}", literals[i]])
            clauses.append([f"~{literals[b-1]}", literals[i]])
        elif gate[0] == 'NOT':
            a = gate[1]
            literals[i] = f"y{i+1}"
            clauses.append([f"~{literals[a-1]}", literals[i]])
    return literals, clauses

def minimal_order(formula):
    n = len(formula)
    A = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        if formula[i].startswith('~'):
            j = int(formula[i][1:]) - 1
            A[j][i] = 1
        else:
            j = int(formula[i]) - 1
            A[j][j] += 1
    gaussian_elimination(A)
    rank = sum(1 for row in A if any(row))
    return rank

def circuit_monotone_width(circuit):
    n = len(circuit)
    max_depth = 0
    stack = [(0, 0)]
    while stack:
        node, depth = stack.pop()
        if node >= n:
            continue
        max_depth = max(max_depth, depth)
        for gate in circuit[node]:
            stack.append((gate-1, depth+1))
    return max_depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):
            circuit = [[random.choice(['AND', 'OR', 'NOT']), random.randint(1, n), random.randint(1, n)] for _ in range(n)]
            literals, clauses = tseitin_formula(circuit)
            formula = [l if not l.startswith('~') else f"~{l[1:]}" for l in literals]
            m_Cphi = minimal_order(formula)
            w_Cphi = circuit_monotone_width(circuit)
            results.append((m_Cphi, w_Cphi))
    mean_m = sum(m for m, _ in results) / len(results)
    mean_w = sum(w for _, w in results) / len(results)
    k = 1.5
    if all(m < k * w for m, w in results):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "m(Cφ) >= k * w(Cφ)"
    return {
        "metric_name": "min_order_over_monotone_width",
        "metric_value": mean_m / mean_w,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_metric = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r < 10) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std=NA support_fraction={support_fraction}")
    elif any(r > 10 for r in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if result > 10)
        print(f"RESULT: FALSIFIED counterexample=\"m(Cφ) > 10\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")