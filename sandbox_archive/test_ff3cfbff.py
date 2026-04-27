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
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def betti_number(clause_set, variable_set):
    n = len(variable_set)
    m = len(clause_set)
    incidence_matrix = [[0] * n for _ in range(m)]
    for i, clause in enumerate(clause_set):
        for var in clause:
            incidence_matrix[i][var] = 1
    A = gaussian_elimination(incidence_matrix)
    rank = sum(1 for row in A if any(row))
    return m - rank

def resolution_width(clause_set):
    n = len(clause_set)
    max_width = 0
    queue = list(range(n))
    while queue:
        clause_index = queue.pop()
        clause = clause_set[clause_index]
        new_clauses = []
        for other_clause in clause_set:
            if not set(clause).intersection(other_clause):
                continue
            new_clause = [var for var in other_clause if var not in clause]
            if len(new_clause) == 1:
                return 1
            new_clauses.append(tuple(sorted(new_clause)))
        queue.extend(set(range(n)) - {clause_index})
        clause_set.extend(new_clauses)
        max_width = max(max_width, len(clause_set))
    return max_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 10, 12, 14, 16, 18, 20]
    results = []
    for n in n_values:
        b1_values = []
        w_values = []
        for _ in range(20):
            clause_set = set()
            variable_set = set()
            while len(clause_set) < 4.26 * n:
                clause = tuple(sorted(random.sample(range(n), 3)))
                if clause not in clause_set:
                    clause_set.add(clause)
                    for var in clause:
                        variable_set.add(var)
            b1 = betti_number(clause_set, variable_set)
            w = resolution_width(clause_set)
            b1_values.append(b1)
            w_values.append(w)
        log_n = [math.log(n) for _ in range(20)]
        a_b1 = sum((log_n[i] - sum(log_n) / len(log_n)) * (b1_values[i] - sum(b1_values) / len(b1_values)) for i in range(len(log_n))) / sum((log_n[i] - sum(log_n) / len(log_n)) ** 2 for i in range(len(log_n)))
        a_w = sum((log_n[i] - sum(log_n) / len(log_n)) * (w_values[i] - sum(w_values) / len(w_values)) for i in range(len(log_n))) / sum((log_n[i] - sum(log_n) / len(log_n)) ** 2 for i in range(len(log_n)))
        r = sum((b1_values[i] - sum(b1_values) / len(b1_values)) * (w_values[i] - sum(w_values) / len(w_values)) for i in range(len(b1_values))) / math.sqrt(sum((b1_values[i] - sum(b1_values) / len(b1_values)) ** 2 for i in range(len(b1_values)))) / math.sqrt(sum((w_values[i] - sum(w_values) / len(w_values)) ** 2 for i in range(len(w_values))))
        results.append({"n": n, "a_b1": a_b1, "a_w": a_w, "r": r})
    mean_a_b1 = sum(result["a_b1"] for result in results) / len(results)
    mean_a_w = sum(result["a_w"] for result in results) / len(results)
    mean_r = sum(result["r"] for result in results) / len(results)
    conjecture_holds = all(0.5 <= result["a_b1"] <= 1.5 and 0.5 <= result["a_w"] <= 1.5 and result["r"] >= 0.7 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Betti Number and Resolution Width",
        "metric_value": mean_a_b1,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    mean_a_b1 = sum(result["a_b1"] for result in results) / len(results)
    mean_a_w = sum(result["a_w"] for result in results) / len(results)
    mean_r = sum(result["r"] for result in results) / len(results)
    support_fraction = sum(0.5 <= result["a_b1"] <= 1.5 and 0.5 <= result["a_w"] <= 1.5 and result["r"] >= 0.7 for result in results) / len(results)
    if all(0.5 <= result["a_b1"] <= 1.5 and 0.5 <= result["a_w"] <= 1.5 and result["r"] >= 0.7 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_a_b1} std=NA support_fraction={support_fraction}")
    elif any(not (0.5 <= result["a_b1"] <= 1.5 and 0.5 <= result["a_w"] <= 1.5 and result["r"] >= 0.7) for result in results):
        print(f"RESULT: FALSIFIED counterexample=mapping_undefined first_failing_seed=NA")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")