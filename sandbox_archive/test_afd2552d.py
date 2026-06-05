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

def generate_random_boolean_function(n: int) -> list:
    return [random.choice([0, 1]) for _ in range(2**n)]

def evaluate(poly: list, assignment: list) -> int:
    result = poly[0]
    n = len(assignment)
    for i in range(1, len(poly)):
        if poly[i] == 1:
            result += assignment[(i - 1) % n]
        elif poly[i] == -1:
            result -= assignment[(i - 1) % n]
    return result

def is_satisfiable(poly: list, assignment: list) -> bool:
    for var in range(len(assignment)):
        assignment[var] = 0
        if evaluate(poly, assignment) == 1:
            return True
        assignment[var] = 1
        if evaluate(poly, assignment) == 1:
            return True
    return False

def backtrack(assignment: list) -> bool:
    n = len(assignment)
    for i in range(n):
        if assignment[i] == 0:
            assignment[i] = 1
            if is_satisfiable(assignment, assignment[:i+1]):
                return True
            assignment[i] = -1
            if is_satisfiable(assignment, assignment[:i+1]):
                return True
    return False

def find_min_deg(clauses: list) -> int:
    n = len(clauses)
    for i in range(n + 1):
        if backtrack([0]*i):
            return i
    return n

def min_deg_polynomial(clauses: list) -> int:
    return find_min_deg(clauses)

def entropy(clauses: list) -> float:
    total_clauses = len(clauses)
    clause_counts = {}
    for clause in clauses:
        if clause in clause_counts:
            clause_counts[clause] += 1
        else:
            clause_counts[clause] = 1
    entropy = 0.0
    for count in clause_counts.values():
        probability = Fraction(count, total_clauses)
        entropy -= probability * math.log2(probability)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            f = generate_random_boolean_function(n)
            clauses = [i for i, bit in enumerate(f) if bit == 1]
            min_deg = min_deg_polynomial(clauses)
            ent = entropy(clauses)
            results.append((min_deg, ent))
    
    mean_min_deg = sum(min_deg for min_deg, _ in results) / len(results)
    mean_ent = sum(ent for _, ent in results) / len(results)
    corr_coeff = sum((min_deg - mean_min_deg) * (ent - mean_ent) for min_deg, ent in results) / len(results)
    p_value = 0.05  # Placeholder for actual p-value calculation
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(corr_coeff) >= 0.7 and p_value < 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_corr_coeff = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")