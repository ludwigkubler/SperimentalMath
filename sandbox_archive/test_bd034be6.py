# auto-injected by SEC sandbox
import collections
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import json
from itertools import product

def generate_3cnf(n, alpha):
    m = int(alpha * n * (n - 1) / 2)
    clauses = set()
    while len(clauses) < m:
        clause = tuple(sorted(random.sample(range(1, n + 1), 3)))
        if random.choice([True, False]):
            clause = (-x for x in clause)
        clauses.add(tuple(abs(x) for x in clause))
    return clauses

def van_der_corput_base2(num, base=2):
    result = []
    while num > 0:
        result.append(int(num % base))
        num //= base
    return result[::-1]

def embed_clause(clause, n):
    points = []
    for literal in clause:
        var = abs(literal)
        sign = -1 if literal < 0 else 1
        digits = van_der_corput_base2(var + n, base=2)
        point = [sign * d / (2 ** len(digits)) for d in digits]
        points.append(point)
    return points

def star_discrepancy(points):
    m = len(points)
    if m == 0:
        return 0
    min_d = float('inf')
    max_d = -float('inf')
    for i, j in product(range(m), repeat=2):
        d = sum(abs(p[i] - q[j]) for p, q in zip(points, points))
        if d < min_d:
            min_d = d
        if d > max_d:
            max_d = d
    return (max_d - min_d) / m

def dpll(clause_set):
    def backtrack(assignment, clause_set):
        if not clause_set:
            return True
        for literal in clause_set[0]:
            new_assignment = assignment[:]
            if literal > 0:
                new_assignment[literal - 1] = True
            else:
                new_assignment[-literal - 1] = False
            if backtrack(new_assignment, [c for c in clause_set if not any(l in c for l in new_assignment)]):
                return True
        return False
    assignment = [False] * (max(clause_set) + 1)
    return backtrack(assignment, clause_set)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [10, 12, 14, 16, 18, 20]
    results = []
    
    for n in n_values:
        alpha = 4.267
        clauses = generate_3cnf(n, alpha)
        points = sum((embed_clause(clause, n) for clause in clauses), [])
        
        if not dpll(clauses):
            D_F = star_discrepancy(points)
            L_F = len(dpll(clauses))
            
            results.append({
                "n": n,
                "D_F": D_F,
                "L_F": L_F
            })
    
    total_dF = sum(result["D_F"] for result in results)
    total_LF = sum(result["L_F"] for result in results)
    mean_DF = total_dF / len(results)
    mean_LF = total_LF / len(results)
    
    support_fraction = sum(0.5 * n * result["D_F"] - 5 <= math.log2(result["L_F"]) <= 4 * n * result["D_F"] + 5 for result in results) / len(results)
    
    if support_fraction >= 0.85:
        return {
            "metric_name": "support_fraction",
            "metric_value": support_fraction,
            "instances_tested": len(results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        for result in results:
            if result["n"] <= 20 and math.log2(result["L_F"]) < 0.4 * result["n"] * result["D_F"] - 5:
                return {
                    "metric_name": "support_fraction",
                    "metric_value": support_fraction,
                    "instances_tested": len(results),
                    "conjecture_holds": False,
                    "counterexample": f"n={result['n']}, D_F={result['D_F']}, L_F={result['L_F']}"
                }
        return {
            "metric_name": "support_fraction",
            "metric_value": support_fraction,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **result}}))