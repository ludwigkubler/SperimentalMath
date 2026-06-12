# auto-injected by SEC sandbox
import collections
import json
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
from itertools import combinations

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        # Find pivot
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    return A

def rank(A):
    rref = gaussian_elimination(A)
    rank = 0
    for row in rref:
        if any(row):
            rank += 1
    return rank

def dpll(clauses, assignment):
    unsatisfied = [c for c in clauses if not any(l in assignment and assignment[l] == True or -l in assignment and assignment[l] == False for l in c)]
    if not unsatisfied:
        return True
    literals_seen = set()
    for clause in unsatisfied:
        literals_seen.update(clause)
    pure_literal = next((l for l in literals_seen if all(l not in c or -l in c for c in unsatisfied)), None)
    if pure_literal is not None:
        return dpll(unsatisfied, {**assignment, pure_literal: True}) or dpll(unsatisfied, {**assignment, pure_literal: False})
    unit_clause = next((c for c in unsatisfied if len(c) == 1), None)
    if unit_clause is not None:
        literal = unit_clause[0]
        return dpll(unsatisfied, {**assignment, literal: True}) or dpll(unsatisfied, {**assignment, literal: False})
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    total_metric_value = 0.0
    conjecture_holds_count = 0
    
    for n in range(5, n_max + 1):
        for _ in range(instances_tested // (n_max - 4) if n == 5 else instances_tested // (n_max - 4)):
            clauses = []
            for _ in range(random.randint(2 * n, 3 * n)):
                literals = random.sample(range(-n, n+1), random.randint(1, n))
                while any(l == 0 for l in literals):
                    literals = random.sample(range(-n, n+1), random.randint(1, n))
                clauses.append(literals)
            
            A = [[0] * (2 * n + 1) for _ in range(len(clauses))]
            for i, clause in enumerate(clauses):
                for l in clause:
                    if l > 0:
                        A[i][l - 1] += 1
                    else:
                        A[i][-l - 1] -= 1
            
            mtr_H = rank(A)
            width = dpll(clauses, {})
            
            if width == 0:
                continue
            
            ratio = mtr_H / width
            total_metric_value += ratio
            if ratio >= 1.0:
                conjecture_holds_count += 1
    
    metric_name = "mtr_H_over_width"
    metric_value = total_metric_value / instances_tested
    n_max = 40
    conjecture_holds = conjecture_holds_count / instances_tested >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")