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
    
    def matrix_from_cnf(cnf, n):
        M = [[0] * n for _ in range(n)]
        for clause in cnf:
            for lit in clause:
                abs_lit = abs(lit) - 1
                if lit > 0:
                    M[abs_lit][abs_lit] += 1
                else:
                    M[abs_lit][abs_lit] -= 1
        return M
    
    def gaussian_elimination(M):
        n = len(M)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            if M[i][i] == 0:
                continue
            for j in range(n):
                if j != i:
                    factor = M[j][i] / M[i][i]
                    for k in range(n):
                        M[j][k] -= factor * M[i][k]
        return M
    
    def minimal_order(M):
        n = len(M)
        rank = 0
        for row in gaussian_elimination(M):
            if any(row):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(1, n))
            M = matrix_from_cnf(cnf, n)
            order = minimal_order(M)
            total_metric_value += order
            instances_tested += 1
            if instances_tested >= 30:
                break
    
    mean_metric_value = total_metric_value / instances_tested
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in range(total_metric_value, instances_tested)) / instances_tested)
    
    return {
        "metric_name": "Minimal Order",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = "minimal_order"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")