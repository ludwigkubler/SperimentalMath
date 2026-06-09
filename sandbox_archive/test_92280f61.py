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
from fractions import Fraction
import math

def generate_cnf(n: int) -> list:
    clauses = []
    for _ in range(2**n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(clause[i] != -clause[j] for i in range(n) for j in range(i+1, n)):
            clauses.append(clause)
    return clauses

def evaluate_cnf(cnf: list, assignment: list) -> bool:
    return any(all(assignment[abs(lit)-1] * lit > 0 for lit in clause) for clause in cnf)

def calculate_renyi_divergence(p: list, alpha: float) -> float:
    if alpha == 1:
        return -sum(pi * math.log2(pi) for pi in p)
    else:
        return (1 / (alpha - 1)) * sum(pi ** alpha for pi in p) - 1

def calculate_resolution_width(cnf: list) -> int:
    n = len(cnf[0])
    clauses = set(tuple(sorted(clause)) for clause in cnf)
    queue = list(clauses)
    while queue:
        clause1, clause2 = queue.pop()
        new_clauses = []
        for lit in range(1, n + 1):
            if (lit,) not in clause1 and (-lit,) not in clause1:
                new_clause = tuple(sorted(set(clause1) | {lit}))
                if new_clause not in clauses:
                    new_clauses.append(new_clause)
            if (-lit,) not in clause2 and (lit,) not in clause2:
                new_clause = tuple(sorted(set(clause2) | {-lit}))
                if new_clause not in clauses:
                    new_clauses.append(new_clause)
        queue.extend(new_clauses)
        clauses.update(new_clauses)
    return len(queue)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        p = [Fraction(1, 2**n)] * (2**n)
        total_metric_value = 0
        
        for _ in range(30):
            assignment = [random.choice([-1, 1]) for _ in range(n)]
            if evaluate_cnf(cnf, assignment):
                p[assignment.index(1)] += Fraction(1, 2**n)
        
        for alpha in [1, float('inf')]:
            renyi_divergence = calculate_renyi_divergence(p, alpha)
            resolution_width = calculate_resolution_width(cnf)
            if resolution_width == 0:
                continue
            ratio = renyi_divergence / resolution_width
            results.append({"n": n, "alpha": alpha, "ratio": ratio})
            total_metric_value += ratio
        
        instances_tested = len(results)
        n_max = max(n_values)
        conjecture_holds = all(result["ratio"] <= 10 for result in results)  # Arbitrary constant c
        counterexample = "" if conjecture_holds else "mapping_undefined"
        
        return {
            "metric_name": "Rényi Divergence Ratio",
            "metric_value": total_metric_value / instances_tested,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")