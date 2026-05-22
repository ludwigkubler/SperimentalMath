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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B[0]), len(B)
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        m = len(A)
        if m == 1:
            return A[0][0]
        det = 0
        for i in range(m):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            det += (-1) ** i * A[0][i] * determinant(submatrix)
        return det
    
    def is_expander(G, n):
        degree_sum = sum(sum(1 for _ in neighbors) for neighbors in G)
        if degree_sum == 0:
            return False
        avg_degree = degree_sum / n
        if avg_degree < 2:
            return False
        max_degree = max(len(neighbors) for neighbors in G)
        if max_degree > 2 * avg_degree:
            return True
        return False
    
    def geometric_entropy(G):
        n = len(G)
        A = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if random.choice([True, False]):
                    A[i][j] = 1
                    A[j][i] = 1
        det_A = determinant(A)
        if det_A == 0:
            return float('inf')
        entropy = -math.log2(det_A / n**n)
        return entropy
    
    def tseitin_formula(G):
        n = len(G)
        formula = []
        for i in range(n):
            clause = [f'x{i}', f'y{i}']
            formula.append(clause)
            for j in range(i+1, n):
                if G[i][j]:
                    clause = [f'x{j}', f'y{i}', f'y{j}']
                    formula.append(clause)
        return formula
    
    def resolution_refutation_length(formula):
        length = 0
        while True:
            new_clauses = []
            for i in range(len(formula)):
                for j in range(i+1, len(formula)):
                    if set(formula[i]).isdisjoint(set(formula[j])):
                        continue
                    common_vars = list(set(formula[i]) & set(formula[j]))
                    for var in common_vars:
                        new_clause = [f'~{var}']
                        for v in formula[i]:
                            if v != var and v[0] == '~':
                                new_clause.append(v[1:])
                        for v in formula[j]:
                            if v != var and v[0] != '~':
                                new_clause.append('~' + v)
                        new_clauses.append(new_clause)
            if not new_clauses:
                break
            formula.extend(new_clauses)
            length += 1
        return length
    
    n = random.randint(5, 40)
    G = [[random.choice([True, False]) for _ in range(n)] for _ in range(n)]
    G = [row[:] for row in G]
    for i in range(n):
        G[i][i] = True
    if not is_expander(G, n):
        return {
            "metric_name": "geometric_entropy",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "non-expander_graph"
        }
    
    H = geometric_entropy(G)
    F = tseitin_formula(G)
    L_F = resolution_refutation_length(F)
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": H / L_F,
        "instances_tested": 1,
        "conjecture_holds": H >= 0.5 * L_F,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"geometric_entropy < 0.5 * resolution_refutation_length\" first_failing_seed={first_failing_seed}")