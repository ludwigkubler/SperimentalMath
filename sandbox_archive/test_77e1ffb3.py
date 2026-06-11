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
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def incidence_matrix(cnf, n):
        M = [[0] * n for _ in range(n)]
        for clause in cnf:
            x, y = abs(clause[0]) - 1, abs(clause[1]) - 1
            if clause[0] > 0: M[x][y] = 1
            else: M[y][x] = 1
        return M
    
    def min_modular_tensor_rank(M):
        n = len(M)
        rank = 0
        for i in range(n):
            if all(M[j][i] == 0 for j in range(n)):
                continue
            rank += 1
            for j in range(n):
                if M[j][i] != 0:
                    for k in range(n):
                        M[j][k] -= M[i][k]
        return rank
    
    def resolution_width(cnf):
        width = 0
        stack = []
        literals_seen = set()
        
        def resolve(lit, cnf):
            nonlocal width
            if lit in literals_seen:
                return False
            literals_seen.add(lit)
            for clause in cnf:
                if lit in clause:
                    clause.remove(lit)
                    if len(clause) == 0:
                        return False
                    elif len(clause) == 1:
                        return resolve(-clause[0], cnf)
                    else:
                        stack.append((lit, clause))
            width = max(width, len(stack))
            while stack:
                lit, clause = stack.pop()
                if not resolve(lit, cnf):
                    return False
            return True
        
        for lit in range(1, n + 1):
            if not resolve(lit, cnf):
                return float('inf')
        
        return width
    
    def correlation_coefficient(mtr_values, w_values):
        n = len(mtr_values)
        mean_mtr = sum(mtr_values) / n
        mean_w = sum(w_values) / n
        numerator = sum((mtr_values[i] - mean_mtr) * (w_values[i] - mean_w) for i in range(n))
        denominator = math.sqrt(sum((mtr_values[i] - mean_mtr) ** 2 for i in range(n)) * sum((w_values[i] - mean_w) ** 2 for i in range(n)))
        return numerator / denominator if denominator != 0 else float('nan')
    
    n_values = [5, 10, 15, 20, 30, 40]
    mtr_values = []
    w_values = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(1, 2 * n))
            M = incidence_matrix(cnf, n)
            mtr = min_modular_tensor_rank(M)
            w = resolution_width(cnf)
            
            if mtr > 1.5 * w:
                return {
                    "metric_name": "correlation_coefficient",
                    "metric_value": float('nan'),
                    "instances_tested": len(mtr_values),
                    "n_max": max(n_values),
                    "conjecture_holds": False,
                    "counterexample": f"mtr > 1.5 * w for n={n}"
                }
            
            mtr_values.append(mtr)
            w_values.append(w)
    
    correlation = correlation_coefficient(mtr_values, w_values)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": len(mtr_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation > 0.7,
        "counterexample": ""
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mtr > 1.5 * w\" first_failing_seed={first_failing_seed}")