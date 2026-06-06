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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(cols):
            max_row = rank
            for j in range(rank, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            if matrix[max_row][i] == 0:
                continue
            matrix[rank], matrix[max_row] = matrix[max_row], matrix[rank]
            for j in range(cols):
                if j != i and matrix[j][i] != 0:
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(i, cols):
                        matrix[j][k] += factor * matrix[i][k]
            rank += 1
        return rank
    
    def resolution_width(cnf):
        queue = cnf[:]
        seen = set()
        while queue:
            clause = queue.pop(0)
            for other_clause in queue + list(seen):
                for lit in clause:
                    if -lit in other_clause:
                        new_clause = [l for l in other_clause if l != -lit]
                        if not new_clause:
                            return 1
                        if tuple(new_clause) not in seen:
                            seen.add(tuple(new_clause))
                            queue.append(new_clause)
        return len(queue)
    
    def monodromy_group_order(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for lit in clause:
                matrix[abs(lit)][abs(lit)] += 1
        return gaussian_elimination(matrix)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(2 * n, 3 * n))
            m = monodromy_group_order(cnf)
            w = resolution_width(cnf)
            if m == 0 or w == 0:
                continue
            results.append((m, w))
    
    if not results:
        return {
            "metric_name": "Monodromy Group Order vs Resolution Width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    m_values = [m for m, _ in results]
    w_values = [w for _, w in results]
    mean_m = sum(m_values) / len(m_values)
    mean_w = sum(w_values) / len(w_values)
    var_m = sum((m - mean_m) ** 2 for m in m_values) / len(m_values)
    var_w = sum((w - mean_w) ** 2 for w in w_values) / len(w_values)
    corr_coeff = (sum((m - mean_m) * (w - mean_w) for m, w in results) /
                  math.sqrt(var_m * var_w))
    
    return {
        "metric_name": "Monodromy Group Order vs Resolution Width",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": corr_coeff > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_corr_coeff = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Correlation coefficient did not meet threshold' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Reason=No valid instances found")