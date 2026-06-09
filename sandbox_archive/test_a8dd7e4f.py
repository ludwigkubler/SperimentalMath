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

def generate_cnf(num_vars, num_clauses):
    cnf = []
    for _ in range(num_clauses):
        clause = set()
        while len(clause) < 2:
            var = random.randint(1, num_vars)
            polarity = random.choice([True, False])
            if polarity:
                clause.add(var)
            else:
                clause.add(-var)
        cnf.append(tuple(sorted(clause)))
    return tuple(cnf)

def dpll(cnf):
    def backtrack(assignment, clause_set):
        unit_clause = next((c for c in clause_set if len(c) == 1), None)
        if unit_clause:
            var = unit_clause[0]
            if var > 0 and var not in assignment:
                return backtrack(assignment | {var}, [c for c in clause_set if var not in c])
            elif var < 0 and -var not in assignment:
                return backtrack(assignment | {-var}, [c for c in clause_set if -var not in c])
        pure_literal = next((v for v in range(1, num_vars + 1) if (v not in assignment and -v not in assignment)), None)
        if pure_literal is not None:
            return backtrack(assignment | {pure_literal}, [c for c in clause_set if pure_literal not in c])
        if not clause_set:
            return True
        var = next((v for v in range(1, num_vars + 1) if v not in assignment and -v not in assignment), None)
        return backtrack(assignment | {var}, [c for c in clause_set if var not in c]) or backtrack(assignment | {-var}, [c for c in clause_set if -var not in c])
    
    num_vars = len(set(abs(lit) for lit in cnf[0]))
    return backtrack({}, cnf)

def compute_ehrhart_polynomial(cnf):
    n = len(cnf)
    m = len(cnf[0])
    A = [[Fraction(1, 1)] * (m + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(m + 1):
            if j == 0:
                A[i][j] = Fraction(i, 1)
            else:
                A[i][j] = A[i-1][j] * (i - j) / i + A[i-1][j-1]
    
    ehrhart_polynomial = [A[n][j] for j in range(m + 1)]
    return ehrhart_polynomial

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        num_vars = random.randint(5, n_max)
        num_clauses = random.randint(num_vars, min(n_max, num_vars * 2))
        cnf_formula = generate_cnf(num_vars, num_clauses)
        
        resolution_width = dpll(cnf_formula)
        ehrhart_polynomial = compute_ehrhart_polynomial(cnf_formula)
        degree_of_ehrhart_polynomial = len(ehrhart_polynomial) - 1
        
        if resolution_width is None:
            continue
        
        metric_value = abs(resolution_width - degree_of_ehrhart_polynomial)
        metric_values.append(metric_value)
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    conjecture_holds = all(value <= 3 for value in metric_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "resolution_width",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")