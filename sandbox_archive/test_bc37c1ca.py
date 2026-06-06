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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if any(clause[i] == -clause[j] for i in range(n) for j in range(i+1, n)):
                clauses.append(clause)
        return clauses
    
    def matrix_representation(cnf):
        n = len(cnf[0])
        M = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for lit in clause:
                i = abs(lit) - 1
                if lit > 0:
                    M[i][n] += 1
                else:
                    M[n][i] += 1
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
            denom = M[i][i]
            for j in range(i, n+1):
                M[i][j] /= denom
            for j in range(n):
                if i != j:
                    factor = M[j][i]
                    for k in range(i, n+1):
                        M[j][k] -= factor * M[i][k]
        return M
    
    def rank(M):
        n = len(M)
        r = 0
        for i in range(n):
            if any(abs(M[i][j]) > 0.0001 for j in range(r, n+1)):
                r += 1
        return r
    
    def variance(values):
        mean = sum(values) / len(values)
        return sum((x - mean)**2 for x in values) / len(values)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        M = matrix_representation(cnf)
        GE_M = gaussian_elimination(M)
        rank_value = rank(GE_M)
        results.append(rank_value)
    
    if len(results) < 30:
        return {
            "metric_name": "variance",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    observed_variance = variance(results)
    expected_variance = math.log(len(n_values))
    
    return {
        "metric_name": "variance",
        "metric_value": observed_variance,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(observed_variance - expected_variance) <= 0.1 * expected_variance,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")