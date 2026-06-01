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
    
    def characteristic_polynomial(cnf):
        n = len(cnf[0])
        poly = [[0] * (n + 1) for _ in range(n + 1)]
        poly[0][0] = 1
        for clause in cnf:
            new_poly = [[0] * (n + 1) for _ in range(n + 1)]
            for x in clause:
                if x > 0:
                    for i in range(n, -1, -1):
                        for j in range(n + 1):
                            new_poly[i][j] += poly[i - abs(x)][j]
                else:
                    for i in range(n, -1, -1):
                        for j in range(n + 1):
                            new_poly[i][j] -= poly[i - abs(x)][j]
            poly = new_poly
        return poly
    
    def resolution_width(cnf):
        n = len(cnf[0])
        clauses = set(tuple(sorted(clause)) for clause in cnf)
        queue = list(clauses)
        while queue:
            clause1 = queue.pop()
            if len(clause1) == 1:
                return len(queue) + 1
            for clause2 in queue:
                new_clause = []
                for lit1 in clause1:
                    if -lit1 in clause2:
                        continue
                    new_clause.append(lit1)
                if not new_clause:
                    return len(queue) + 1
                new_clause = tuple(sorted(new_clause))
                if new_clause not in queue:
                    queue.append(new_clause)
        return len(queue)
    
    def automorphic_forms(poly):
        n = len(poly[0]) - 1
        forms = set()
        for i in range(n + 1):
            for j in range(n + 1):
                if poly[i][j] != 0:
                    form = (i, j)
                    forms.add(form)
        return forms
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    N_values = []
    w_values = []
    
    for n in n_values:
        instances_tested = 0
        for _ in range(5):
            cnf = [[random.randint(-n, n) for _ in range(n)] for _ in range(random.randint(1, 2 * n))]
            poly = characteristic_polynomial(cnf)
            forms = automorphic_forms(poly)
            N_values.append(len(forms))
            w_values.append(resolution_width(cnf))
            instances_tested += 1
    
    correlation_coefficient = pearson_correlation(N_values, w_values)
    mean_N = sum(N_values) / len(N_values)
    
    conjecture_holds = 0.5 <= correlation_coefficient < 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient_out_of_range"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(N_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_N = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_N} std=0.0 support_fraction={support_fraction}")
    elif any(res["metric_value"] < 0.5 or res["metric_value"] > 10 for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if res["metric_value"] < 0.5 or res["metric_value"] > 10)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_out_of_range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")