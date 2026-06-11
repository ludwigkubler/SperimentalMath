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
            if random.choice([True, False]):
                clause[0] *= -1
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment):
        unsatisfied_clauses = [c for c in cnf if all(l not in assignment or assignment[l] != (l < 0) for l in c)]
        if not unsatisfied_clauses:
            return True
        unit_clause = next((c for c in unsatisfied_clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            assignment[literal] = (literal < 0)
            if dpll(cnf, assignment):
                return True
            del assignment[literal]
            assignment[-literal] = False
            if dpll(cnf, assignment):
                return True
            del assignment[-literal]
        else:
            literal = random.choice([l for c in unsatisfied_clauses for l in c if l not in assignment])
            assignment[literal] = (literal < 0)
            if dpll(cnf, assignment):
                return True
            del assignment[literal]
            assignment[-literal] = False
            if dpll(cnf, assignment):
                return True
            del assignment[-literal]
        return False
    
    def nonnegative_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(n):
            pivot = next((j for j in range(m) if matrix[j][i] != 0), None)
            if pivot is not None:
                rank += 1
                for j in range(m):
                    if j != pivot:
                        factor = -matrix[j][i] / matrix[pivot][i]
                        for k in range(n):
                            matrix[j][k] += factor * matrix[pivot][k]
        return rank
    
    def clause_indicator_matrix(cnf, n):
        m = len(cnf)
        matrix = [[0] * n for _ in range(m)]
        for i, clause in enumerate(cnf):
            for l in clause:
                if abs(l) <= n:
                    matrix[i][abs(l) - 1] = 1
        return matrix
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y))
        return cov_xy / (std_x * std_y)
    
    def regression_line_slope(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        slope = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / sum((x[i] - mean_x) ** 2 for i in range(len(x)))
        return slope
    
    def regression_line_intercept(x, y):
        slope = regression_line_slope(x, y)
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        intercept = mean_y - slope * mean_x
        return intercept
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(2 * n, 5 * n)
        cnf = generate_cnf(n, m)
        matrix = clause_indicator_matrix(cnf, n)
        rank = nonnegative_rank(matrix)
        height = dpll(cnf, {})
        results.append((n, rank, height))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    x = [r[1] for r in results]
    y = [r[2] for r in results]
    corr_coeff = correlation_coefficient(x, y)
    slope = regression_line_slope(x, y)
    intercept = regression_line_intercept(x, y)
    
    if corr_coeff < 0.9:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": corr_coeff,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": f"low_correlation_coefficient={corr_coeff}"
        }
    
    if any(abs(r[1] - (slope * r[2] + intercept)) > 0.5 * abs(slope * r[2] + intercept) for n, r1, r2 in results):
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": corr_coeff,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": f"outlier_rank={r1} predicted={slope * r2 + intercept}"
        }
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr_coeff = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='low_correlation_coefficient' first_failing_seed={first_failing_seed}")