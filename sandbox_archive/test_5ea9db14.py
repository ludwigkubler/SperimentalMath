# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for r in range(i+1, n):
            if abs(A[r][i]) > abs(A[max_row][i]):
                max_row = r
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        factor = -A[i][i]
        for k in range(i, n):
            A[i][k] /= factor
        for r in range(i+1, n):
            factor = A[r][i]
            for k in range(i, n):
                if i == k:
                    A[r][k] = 0
                else:
                    A[r][k] += factor * A[i][k]

def betti_number(clause_set, variable_set):
    n = len(variable_set)
    m = len(clause_set)
    
    incidence_matrix = [[0 for _ in range(n)] for _ in range(m)]
    for j, clause in enumerate(clause_set):
        for var in clause:
            incidence_matrix[j][variable_set.index(var)] = 1
    
    gaussian_elimination(incidence_matrix)
    
    rank = sum(1 for row in incidence_matrix if any(row))
    return rank - 1

def resolution_width(clause_set, variable_set):
    n = len(variable_set)
    m = len(clause_set)
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if sum(1 for v in c if v in assignment) == 0 and sum(1 for v in c if -v in assignment) == 0), None)
        if unit_clause:
            literal = next(v for v in unit_clause if v not in assignment)
            return dpll([c for c in clauses if literal not in c and -literal not in c], assignment + [literal])
        
        pure_literal = next((v for v in variable_set if sum(1 for c in clauses if v in c) == 0), None)
        if pure_literal:
            return dpll(clauses, assignment + [pure_literal])
        
        literal = random.choice(variable_set)
        return dpll(clauses, assignment + [literal]) or dpll(clauses, assignment + [-literal])
    
    max_width = 0
    for _ in range(100):
        assignment = []
        width = 0
        while not dpll(clause_set, assignment):
            literal = random.choice(variable_set)
            if literal not in assignment and -literal not in assignment:
                assignment.append(literal)
                width += 1
        max_width = max(max_width, width)
    
    return max_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 10, 12, 14, 16, 18, 20]
    results = []
    
    for n in n_values:
        clause_set = set()
        variable_set = set()
        
        for _ in range(int(4.26 * n)):
            variables = random.sample(variable_set, 3)
            clause = tuple(sorted(variables))
            clause_set.add(clause)
            for var in variables:
                variable_set.add(var)
        
        b1 = betti_number(clause_set, variable_set)
        w = resolution_width(clause_set, variable_set)
        
        results.append({
            "n": n,
            "b1": b1,
            "w": w
        })
    
    if not results:
        return {
            "metric_name": "Betti Number and Resolution Width",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log_n_values = [math.log(n) for n in n_values]
    log_b1_values = [math.log(result["b1"]) for result in results]
    log_w_values = [math.log(result["w"]) for result in results]
    
    a_b1, a_w = sum(log_b1 * ln_n for log_b1, ln_n in zip(log_b1_values, log_n_values)) / sum(ln_n**2 for ln_n in log_n_values), \
                sum(log_w * ln_n for log_w, ln_n in zip(log_w_values, log_n_values)) / sum(ln_n**2 for ln_n in log_n_values)
    
    r = sum((log_b1 - a_b1 * ln_n) * (log_w - a_w * ln_n) for log_b1, log_w, ln_n in zip(log_b1_values, log_w_values, log_n_values)) / \
        math.sqrt(sum((log_b1 - a_b1 * ln_n)**2 for log_b1, ln_n in zip(log_b1_values, log_n_values)) * sum((log_w - a_w * ln_n)**2 for log_w, ln_n in zip(log_w_values, log_n_values)))
    
    return {
        "metric_name": "Betti Number and Resolution Width",
        "metric_value": {"a_b1": a_b1, "a_w": a_w},
        "instances_tested": len(results),
        "conjecture_holds": 0.5 <= a_b1 <= 1.5 and 0.5 <= a_w <= 1.5 and r >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_a_b1 = sum(r["metric_value"]["a_b1"] for r in results) / len(results)
        mean_a_w = sum(r["metric_value"]["a_w"] for r in results) / len(results)
        support_fraction = len([r for r in results if "conjecture_holds" in r and r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean_a_b1={mean_a_b1} mean_a_w={mean_a_w} support_fraction={support_fraction}")
    elif any("conjecture_holds" in r and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" in r and not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")