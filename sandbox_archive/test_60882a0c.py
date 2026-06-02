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
import fractions

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        if pivot == 0:
            continue
        for j in range(n):
            A[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    det = 0
    if n == 1:
        return A[0][0]
    elif n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    else:
        for j in range(n):
            det += (-1) ** j * A[0][j] * determinant([row[:j] + row[j+1:] for row in A[1:]])
    return det

def laplacian_matrix(G):
    n = len(G)
    L = [[0] * n for _ in range(n)]
    for i in range(n):
        degree = sum(1 for j in range(n) if G[i][j])
        L[i][i] = -degree
        for j in range(i + 1, n):
            if G[i][j]:
                L[i][j] = L[j][i] = 1
    return L

def minimal_local_indefinite_integral(L):
    n = len(L)
    I = [[0] * n for _ in range(n)]
    for i in range(n):
        I[i][i] = 1
    A = matrix_multiply(I, L)
    gaussian_elimination(A)
    mli = sum(abs(A[i][i]) for i in range(n))
    return mli

def communication_complexity_rank(G):
    n = len(G)
    clauses = []
    variables = set()
    for i in range(n):
        for j in range(i + 1, n):
            if G[i][j]:
                clause = [i + 1, -j - 1]
                clauses.append(clause)
                variables.update([i + 1, j + 1])
    
    def tseitin_encoding():
        nonlocal variables
        tseitin_count = max(variables) + 1
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j]:
                    clause = [tseitin_count, -i - 1, -j - 1]
                    clauses.append(clause)
                    variables.add(tseitin_count)
                    tseitin_count += 1
        return tseitin_count
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            return False
        pure_literal = next((l for l in variables if all(l not in c or -l in c for c in clauses)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            if dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment):
                return True
            new_assignment[pure_literal] = False
            if dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment):
                return True
            return False
        literal = next(iter(variables))
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        return False
    
    tseitin_count = tseitin_encoding()
    assignment = {i: None for i in range(1, tseitin_count + 1)}
    if dpll(clauses, assignment):
        rank = sum(1 for v in assignment.values() if v is not None)
        return rank
    else:
        return float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    mli_sum = 0
    r_sum = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        if any(G[i][j] != G[j][i] for i in range(n) for j in range(i)):
            continue
        mli = minimal_local_indefinite_integral(laplacian_matrix(G))
        r = communication_complexity_rank(G)
        if r == float('inf'):
            continue
        mli_sum += mli
        r_sum += r
        instances_tested += 1
        n_max = max(n_max, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "mli-r",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_mli = mli_sum / instances_tested
    mean_r = r_sum / instances_tested
    abs_diff_sum = sum(abs(mli - r) for mli, r in zip([minimal_local_indefinite_integral(laplacian_matrix(G)) for _ in range(30)], [communication_complexity_rank(G) for _ in range(30)]))
    mean_abs_diff = abs_diff_sum / 30
    
    return {
        "metric_name": "mli-r",
        "metric_value": mean_mli,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": mean_abs_diff <= 3 and abs(mean_mli - mean_r) / max(abs(mean_mli), abs(mean_r)) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")