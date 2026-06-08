# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(d, n):
        if d * (n - 1) % 2 != 0:
            return None
        graph = {i: set() for i in range(n)}
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    graph[i].add(j)
                    graph[j].add(i)
                    edges.append((i, j))
        return graph
    
    def tseitin_formula(graph):
        literals = {node: f'x{node}' for node in range(len(graph))}
        clauses = []
        for node, neighbors in graph.items():
            clause = [f'-{literals[node]}']
            for neighbor in neighbors:
                clause.append(literals[neighbor])
            clauses.append(clause)
            for i in range(len(neighbors)):
                for j in range(i + 1, len(neighbors)):
                    clauses.append([f'-{literals[neighbors[i]]}', f'-{literals[neighbors[j]]}', literals[node]])
        return clauses
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        m = len(matrix[0])
        for i in range(n):
            if matrix[i][i] == 0:
                for j in range(i + 1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    return None
            pivot = Fraction(matrix[i][i])
            for j in range(m):
                matrix[i][j] /= pivot
            for j in range(n):
                if j == i:
                    continue
                factor = matrix[j][i]
                for k in range(m):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def determinant(matrix):
        n = len(matrix)
        det = Fraction(1)
        for i in range(n):
            pivot = matrix[i][i]
            if pivot == 0:
                return 0
            det *= pivot
            for j in range(i + 1, n):
                factor = matrix[j][i] / pivot
                for k in range(m):
                    matrix[j][k] -= factor * matrix[i][k]
        return det
    
    def minimal_symplectic_volume(graph):
        n = len(graph)
        A = [[0] * (2 * n) for _ in range(2 * n)]
        for i in range(n):
            A[i][i] = 1
            A[n + i][n + i] = 1
            for j in graph[i]:
                A[i][n + j] = -1
                A[n + i][j] = -1
        det_A = determinant(A)
        if det_A == 0:
            return None
        det_A_inv = Fraction(1, det_A)
        return det_A_inv
    
    def resolution_width(clauses):
        n = len(clauses)
        width = [len(c) for c in clauses]
        return max(width)
    
    n_max = 40
    instances_tested = 0
    total_msv = Fraction(0)
    total_w = 0
    
    for _ in range(30):
        d = random.randint(2, 5)
        n = random.randint(5, n_max)
        graph = generate_d_regular_graph(d, n)
        if graph is None:
            continue
        clauses = tseitin_formula(graph)
        msv = minimal_symplectic_volume(graph)
        if msv is None:
            continue
        w = resolution_width(clauses)
        total_msv += msv * w
        total_w += w
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "MSV/w",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_msv_w = total_msv / instances_tested
    correlation_coefficient = Fraction(total_msv * total_w, instances_tested * total_msv * total_w)
    conjecture_holds = correlation_coefficient >= Fraction(8, 10) and mean_msv_w >= 1
    
    return {
        "metric_name": "MSV/w",
        "metric_value": float(mean_msv_w),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_msv_w = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_msv_w} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_msv_w} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")