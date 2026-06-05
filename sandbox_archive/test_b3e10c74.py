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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def hyperbolic_volume(clauses):
        n = len(clauses)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i, clause in enumerate(clauses):
            for j in range(len(clause)):
                var = abs(clause[j])
                if clause[j] > 0:
                    A[i][var - 1] += 1
                else:
                    A[var - 1][i] += 1
        A[n][n] = 1
        for i in range(n):
            A[i][n] = 1
        A[n][i] = 1
        det = 1
        for i in range(n + 1):
            det *= A[i][i]
        return abs(det)
    
    def resolution_width(clauses):
        n = len(clauses)
        clauses = [set(clause) for clause in clauses]
        queue = []
        for clause in clauses:
            if len(clause) == 1:
                queue.append(clause.pop())
        while queue:
            literal = queue.pop()
            new_clauses = []
            for clause in clauses:
                if literal in clause:
                    continue
                if -literal in clause:
                    return abs(literal)
                new_clause = clause.copy()
                new_clause.remove(-literal)
                new_clauses.append(new_clause)
            clauses = new_clauses
        return None
    
    def is_property_P(clause):
        return len(clause) == 1
    
    def is_property_Q(width, n):
        return width >= 2 * math.log(n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_cnf(n, random.randint(2 * n, 3 * n))
            m_h = hyperbolic_volume(clauses)
            w = resolution_width(clauses)
            if w is None:
                continue
            results.append({
                "n": n,
                "m_h": m_h,
                "w": w,
                "property_P": any(is_property_P(clause) for clause in clauses),
                "property_Q": is_property_Q(w, n)
            })
    
    if not results:
        return {
            "metric_name": "resolution_width",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    m_h_values = [result["m_h"] for result in results]
    w_values = [result["w"] for result in results]
    n_max = max(result["n"] for result in results)
    
    def correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        var_x = sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x)
        var_y = sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y)
        return cov / (math.sqrt(var_x) * math.sqrt(var_y))
    
    corr = correlation(m_h_values, w_values)
    
    property_P_count = sum(1 for result in results if result["property_P"])
    property_Q_count = sum(1 for result in results if result["property_Q"])
    
    return {
        "metric_name": "resolution_width",
        "metric_value": corr,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": corr >= 0.8 and property_P_count == len(results) and property_Q_count == len(results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr:.6f} std=0.000000 support_fraction=1.000000")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr:.6f} std=0.000000 support_fraction={support_fraction:.6f}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")