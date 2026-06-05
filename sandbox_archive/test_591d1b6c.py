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
    
    def generate_sat_formula(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def nnf(sat_formula):
        n = int(math.log2(len(sat_formula)))
        nnf_formula = []
        for i in range(n):
            clause = []
            for j in range(i+1, n):
                if sat_formula[2**(i+j)] == 0:
                    clause.append(j)
            if clause:
                nnf_formula.append(clause)
        return nnf_formula
    
    def lid(nnf_formula):
        variables = set()
        for clause in nnf_formula:
            variables.update(clause)
        return len(variables)
    
    def ccr(sat_formula):
        n = int(math.log2(len(sat_formula)))
        matrix = [[0] * (n+1) for _ in range(n+1)]
        for i in range(2**n):
            row = [i >> j & 1 for j in range(n)]
            row.append(sat_formula[i])
            matrix[row[0]] = row
        rank = 0
        for i in range(n+1):
            if any(matrix[j][i] for j in range(i, n+1)):
                pivot_row = next(j for j in range(i, n+1) if matrix[j][i])
                matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
                rank += 1
                for j in range(n+1):
                    if i != j:
                        factor = Fraction(matrix[j][i], matrix[i][i])
                        for k in range(n+1):
                            matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x)**2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y)**2 for i in range(n)) / n
        return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))
    
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
    conjecture_holds = 0.5 < correlation < 0.7
    counterexample = "" if conjecture_holds else f"Correlation: {correlation}"
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
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
        print(f"RESULT: FALSIFIED counterexample='Correlation outside [0.5, 0.7]' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient statistical signal")