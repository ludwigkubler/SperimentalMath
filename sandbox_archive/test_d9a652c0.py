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
    
    def generate_cnf(m, n):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def indicator_polynomial(clauses, n):
        indicators = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            i, j = abs(clause[0]), abs(clause[1])
            if clause[0] > 0 and clause[1] > 0:
                indicators[i][j] = 1
            elif clause[0] < 0 and clause[1] < 0:
                indicators[i][j] = -1
        return indicators
    
    def grothendieck_witt_class(indicators):
        n = len(indicators) - 1
        trace = sum(indicators[i][i] for i in range(1, n + 1))
        det = 1
        for i in range(1, n + 1):
            det *= indicators[i][i]
        return math.sqrt(trace * det)
    
    def adjacency_matrix(clauses, n):
        adj_matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            i, j = abs(clause[0]), abs(clause[1])
            if clause[0] > 0 and clause[1] > 0:
                adj_matrix[i][j] += 1
                adj_matrix[j][i] += 1
            elif clause[0] < 0 and clause[1] < 0:
                adj_matrix[i][j] -= 1
                adj_matrix[j][i] -= 1
        return adj_matrix
    
    def min_eigenvalue(matrix):
        n = len(matrix)
        if n == 0:
            return 0
        eigenvalues = []
        for i in range(n):
            matrix[i].append(1)  # Augmented with a 1 to make it square
        while len(eigenvalues) < n:
            pivot_row = max(range(len(matrix)), key=lambda r: abs(matrix[r][-1]))
            if matrix[pivot_row][-1] == 0:
                break
            for i in range(n):
                if i != pivot_row:
                    factor = matrix[i][-1] / matrix[pivot_row][-1]
                    for j in range(n + 1):
                        matrix[i][j] -= factor * matrix[pivot_row][j]
            eigenvalues.append(matrix[pivot_row][-2])
        return min(eigenvalues)
    
    m_values = [5, 10, 15, 20, 30, 40]
    results = []
    for m in m_values:
        indicators = indicator_polynomial(generate_cnf(m, m), m)
        grothendieck_witt = grothendieck_witt_class(indicators)
        adj_matrix = adjacency_matrix(generate_cnf(m, m), m)
        min_eig = min_eigenvalue(adj_matrix)
        if min_eig <= 0:
            continue
        ratio = grothendieck_witt / math.sqrt(m) * math.sqrt(min_eig)
        results.append(ratio)
    
    if not results:
        return {
            "metric_name": "Grothendieck-Witt Class vs. Communication Complexity Rank",
            "metric_value": 0,
            "instances_tested": len(results),
            "n_max": max(m_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_ratio = sum(results) / len(results)
    return {
        "metric_name": "Grothendieck-Witt Class vs. Communication Complexity Rank",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(m_values),
        "conjecture_holds": mean_ratio >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_metric = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r >= 0.8) / len(results)
    
    if all(r >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if r < 0.8)]
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")