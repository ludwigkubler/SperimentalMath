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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        if random.choice([True, False]):
            clause[0] *= -1
        if random.choice([True, False]):
            clause[1] *= -1
        cnf.append(clause)
    return cnf

def count_satisfying_assignments(cnf):
    n = max(abs(lit) for lit in sum(cnf, []))
    assignments = [0] * (2 ** n)
    
    def is_satisfying(assignment):
        for clause in cnf:
            if all(assignment[abs(lit) - 1] != (lit < 0) for lit in clause):
                return False
        return True
    
    count = 0
    for i in range(len(assignments)):
        assignment = [(i >> j) & 1 for j in range(n)]
        if is_satisfying(assignment):
            count += 1
    return count

def compute_second_betti_number(cnf):
    n = max(abs(lit) for lit in sum(cnf, []))
    incidence_matrix = [[0] * (n + 2) for _ in range(n + 2)]
    
    for clause in cnf:
        for i in range(1, n + 1):
            if i in clause:
                incidence_matrix[i][i] += 1
            else:
                incidence_matrix[i][-2] += 1
                incidence_matrix[-1][i] += 1
    
    # Gaussian elimination to find the rank of the matrix
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(cols):
                if i != j:
                    factor = Fraction(matrix[j][i], matrix[i][i])
                    for k in range(rows):
                        matrix[j][k] -= factor * matrix[i][k]
        
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
        return rank
    
    rank = gaussian_elimination(incidence_matrix)
    return (n + 2 - rank) // 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    t_F_values = []
    H2_F_values = []
    
    for n in n_values:
        cnf = generate_cnf(n, int(1.5 * n))
        t_F = count_satisfying_assignments(cnf)
        H2_F = compute_second_betti_number(cnf)
        
        t_F_values.append(t_F)
        H2_F_values.append(H2_F)
    
    correlation_coefficient = sum((t_F - mean_t_F) * (H2_F - mean_H2_F) for t_F, H2_F in zip(t_F_values, H2_F_values)) / len(t_F_values)
    mean_t_F = sum(t_F_values) / len(t_F_values)
    mean_H2_F = sum(H2_F_values) / len(H2_F_values)
    
    conjecture_holds = correlation_coefficient > 0.7 and all(H2_F <= 20 for H2_F in H2_F_values)
    counterexample = "" if conjecture_holds else "H^2_F > 20"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(t_F_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")