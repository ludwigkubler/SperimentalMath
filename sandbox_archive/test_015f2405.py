# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, product

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        i_max = next((i for i in range(rank, m) if A[i][j] != 0), None)
        if i_max is not None:
            A[rank], A[i_max] = A[i_max], A[rank]
            for i in range(m):
                if i != rank:
                    factor = -A[i][j] / A[rank][j]
                    for k in range(n):
                        A[i][k] += factor * A[rank][k]
            rank += 1
    return rank

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def random_cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        literals = random.sample(variables, random.randint(1, n))
        clause = [random.choice([l, -l]) for l in literals]
        clauses.append(clause)
    return clauses

def dpll(clauses, assignment=None):
    if assignment is None:
        assignment = {}
    unit_clauses = [c[0] for c in clauses if len(c) == 1 and c[0] not in assignment]
    while unit_clauses:
        literal = unit_clauses.pop()
        assignment[literal] = True
        new_clauses = []
        for clause in clauses:
            if literal in clause:
                continue
            elif -literal in clause:
                new_clauses.append([l for l in clause if l != -literal])
            else:
                new_clauses.append(clause)
        clauses = new_clauses
        unit_clauses.extend([c[0] for c in clauses if len(c) == 1 and c[0] not in assignment])

    pure_literals = [l for l in range(1, n + 1) if all(l not in clause or -l not in clause for clause in clauses)]
    while pure_literals:
        literal = pure_literals.pop()
        assignment[literal] = True
        new_clauses = []
        for clause in clauses:
            if literal in clause:
                continue
            elif -literal in clause:
                new_clauses.append([l for l in clause if l != -literal])
            else:
                new_clauses.append(clause)
        clauses = new_clauses

    return len(clauses) == 0

def resolution_width(clauses):
    queue = [c[:] for c in clauses]
    while True:
        unit_clause = next((c for c in queue if len(c) == 1), None)
        if unit_clause is None:
            break
        literal = unit_clause[0]
        new_clauses = []
        for clause in queue:
            if literal in clause:
                continue
            elif -literal in clause:
                new_clauses.append([l for l in clause if l != -literal])
            else:
                new_clauses.append(clause)
        queue = new_clauses + [c1 + c2 for c1, c2 in combinations(queue, 2) if literal in c1 and -literal in c2]
    return len(queue)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    
    for n in n_values:
        instances_tested = 0
        total_rank = 0
        total_width = 0
        
        for _ in range(30):
            clauses = random_cnf(n, n)
            rank = gaussian_elimination([[1 if l == var else -1 if l == -var else 0 for var in range(1, n + 1)] for clause in clauses])
            width = resolution_width(clauses)
            
            total_rank += rank
            total_width += width
            instances_tested += 1
        
        metrics.append({
            "n": n,
            "avg_rank": total_rank / instances_tested,
            "avg_width": total_width / instances_tested
        })
    
    if not metrics:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    avg_rank = sum(m["avg_rank"] for m in metrics) / len(metrics)
    avg_width = sum(m["avg_width"] for m in metrics) / len(metrics)
    correlation_coefficient = 0
    
    if avg_rank != 0 and avg_width != 0:
        covariance = sum((m["avg_rank"] - avg_rank) * (m["avg_width"] - avg_width) for m in metrics) / len(metrics)
        rank_variance = sum((m["avg_rank"] - avg_rank) ** 2 for m in metrics) / len(metrics)
        width_variance = sum((m["avg_width"] - avg_width) ** 2 for m in metrics) / len(metrics)
        correlation_coefficient = covariance / math.sqrt(rank_variance * width_variance)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": correlation_coefficient,
        "instances_tested": sum(m["instances_tested"] for m in metrics),
        "n_max": max(m["n"] for m in metrics),
        "conjecture_holds": abs(correlation_coefficient) > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")