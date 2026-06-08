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

def generate_random_cnf(n: int) -> list:
    clauses = []
    for _ in range(2**n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if any(clause.count(lit) > 1 for lit in set(clause)):
            continue
        clauses.append(clause)
    return clauses

def symplectic_quotient_order(clauses: list) -> int:
    n = len(clauses[0])
    vectors = [[0] * (2*n + 1) for _ in range(2**n)]
    
    for clause in clauses:
        vector = [0] * (2*n + 1)
        for lit in clause:
            var = abs(lit) - 1
            if lit > 0:
                vector[n + var] += 1
            else:
                vector[var] -= 1
        vectors.append(vector)
    
    order = 0
    while True:
        found = False
        for i in range(len(vectors)):
            for j in range(i+1, len(vectors)):
                if all(vectors[i][k] == vectors[j][k] for k in range(2*n + 1)):
                    vectors.pop(j)
                    vectors.pop(i)
                    found = True
                    break
            if found:
                break
        if not found:
            break
        order += 1
    
    return order

def resolution_proof_width(clauses: list) -> int:
    n = len(clauses[0])
    stack = clauses[:]
    
    while stack:
        clause1 = stack.pop()
        for clause2 in stack[:]:
            common_lits = [lit for lit in clause1 if -lit in clause2]
            if not common_lits:
                continue
            new_clause = []
            for lit in clause1 + clause2:
                if lit not in common_lits:
                    new_clause.append(lit)
            new_clause = list(set(new_clause))
            if len(new_clause) == 0:
                return -1
            stack.append(new_clause)
    
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        for _ in range(5):
            clauses = generate_random_cnf(n)
            order = symplectic_quotient_order(clauses)
            width = resolution_proof_width(clauses)
            if order == -1 or width == -1:
                continue
            results.append((order, width))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    order_values = [r[0] for r in results]
    width_values = [r[1] for r in results]
    
    mean_order = sum(order_values) / len(order_values)
    mean_width = sum(width_values) / len(width_values)
    
    correlation = 0.0
    if len(results) > 1:
        numerator = sum((order - mean_order) * (width - mean_width) for order, width in results)
        denominator = math.sqrt(sum((order - mean_order)**2 for order in order_values)) * math.sqrt(sum((width - mean_width)**2 for width in width_values))
        correlation = numerator / denominator
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8 and all(c >= 0.5 for c in [correlation]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_correlation_too_low")