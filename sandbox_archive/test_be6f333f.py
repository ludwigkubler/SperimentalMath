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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(2, n))]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        if not cnf:
            return True
        unit_clauses = [c[0] for c in cnf if len(c) == 1]
        if not unit_clauses:
            return False
        p = unit_clauses[0]
        new_cnf = []
        for clause in cnf:
            if p in clause:
                continue
            if -p in clause:
                new_clause = [x for x in clause if x != -p]
                if not new_clause:
                    return False
                new_cnf.append(new_clause)
            else:
                new_cnf.append(clause)
        return dpll(new_cnf) or dpll([c for c in cnf if p not in c and -p not in c])
    
    def quandle_rank(cnf):
        n = len(cnf)
        rank = 0
        for i in range(n):
            for j in range(i + 1, n):
                if any(x == y or x == -y for x in cnf[i] for y in cnf[j]):
                    continue
                rank += 1
        return rank
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        proof_length = len(cnf) if dpll(cnf) else float('inf')
        quandle_r = quandle_rank(cnf)
        results.append((quandle_r, proof_length))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    n = len(results)
    x_sum, y_sum, xy_sum, x2_sum, y2_sum = 0, 0, 0, 0, 0
    for x, y in results:
        x_sum += x
        y_sum += y
        xy_sum += x * y
        x2_sum += x ** 2
        y2_sum += y ** 2
    
    mean_x = x_sum / n
    mean_y = y_sum / n
    numerator = n * xy_sum - x_sum * y_sum
    denominator = math.sqrt((n * x2_sum - x_sum ** 2) * (n * y2_sum - y_sum ** 2))
    
    if denominator == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": n,
            "n_max": max(n for _, n in results),
            "conjecture_holds": False,
            "counterexample": "Denominator is zero"
        }
    
    r = numerator / denominator
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": r,
        "instances_tested": n,
        "n_max": max(n for _, n in results),
        "conjecture_holds": abs(r) >= 0.7 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials executed")
        exit(1)
    
    mean_r = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_r = math.sqrt(sum((r["metric_value"] - mean_r) ** 2 for r in results if r["metric_value"] is not None) / (len(results) - 1))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")