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
    
    def generate_sat_formula(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def nnf(sat_formula):
        n = len(sat_formula[0])
        nnf_formula = []
        for clause in sat_formula:
            new_clause = []
            for literal in clause:
                if literal < 0:
                    new_clause.append(-literal)
                else:
                    new_clause.append(literal)
            nnf_formula.append(new_clause)
        return nnf_formula
    
    def lid(nnf_formula):
        n = len(nnf_formula[0])
        seen_vars = set()
        for clause in nnf_formula:
            for literal in clause:
                seen_vars.add(abs(literal))
        return len(seen_vars)
    
    def ccr(sat_formula):
        n = len(sat_formula[0])
        truth_table = [[0] * (2**n) for _ in range(n)]
        for i in range(2**n):
            for j in range(n):
                truth_table[j][i] = 1 if sum([sat_formula[k][(i >> k) & 1] for k in range(n)]) >= 1 else 0
        matrix = []
        for row in truth_table:
            matrix.append(row + [sum(row)])
        rank = 0
        for i in range(n):
            if matrix[i][n]:
                rank += 1
                for j in range(i+1, n):
                    if matrix[j][n]:
                        factor = matrix[j][i] / matrix[i][i]
                        for k in range(n + 1):
                            matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    lid_values = []
    ccr_values = []
    
    for n in n_values:
        sat_formula = generate_sat_formula(n)
        nnf_formula = nnf(sat_formula)
        lid_value = lid(nnf_formula)
        ccr_value = ccr(sat_formula)
        lid_values.append(lid_value)
        ccr_values.append(ccr_value)
    
    correlation = pearson_correlation(lid_values, ccr_values)
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": 0.5 < correlation <= 0.7,
        "counterexample": "" if 0.5 < correlation <= 0.7 else f"Correlation out of range: {correlation}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation out of range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")