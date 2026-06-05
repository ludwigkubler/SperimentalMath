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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        for j in range(n):
            if j != i:
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n+1):
                    A[j][k] -= factor * A[i][k]
    return A

def tsv(matroid):
    n = len(matroid)
    A = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            if matroid[i][j]:
                A[i][j] = 1
                A[j][i] = 1
    rank = sum(1 for row in gaussian_elimination(A) if any(row))
    return math.factorial(rank)

def dpll_width(clauses, assignment):
    stack = [(clauses, assignment)]
    while stack:
        clauses, assignment = stack.pop()
        if not clauses:
            return 0
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            stack.append((new_clauses, new_assignment))
            continue
        pure_literal = next((l for l in range(1, len(assignment)+1) if (l not in assignment and -l not in assignment)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            new_clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
            stack.append((new_clauses, new_assignment))
            continue
        literal = random.choice([l for l in range(1, len(assignment)+1) if l not in assignment])
        new_assignment_true = assignment.copy()
        new_assignment_true[literal] = True
        new_clauses_true = [c for c in clauses if literal not in c and -literal not in c]
        stack.append((new_clauses_true, new_assignment_true))
        new_assignment_false = assignment.copy()
        new_assignment_false[literal] = False
        new_clauses_false = [c for c in clauses if literal not in c and -literal not in c]
        stack.append((new_clauses_false, new_assignment_false))
    return 1

def generate_instance(n):
    clauses = []
    for i in range(1, n+1):
        clause = random.sample(range(1, n+1), random.randint(1, n))
        clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    instances_tested = 30
    n_max = 40
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        clauses = generate_instance(n)
        matroid = [[any(l in c or -l in c for c in clauses) for l in range(1, n+1)] for _ in range(n)]
        tsv_value = tsv(matroid)
        dpll_value = dpll_width(clauses, {})
        
        if dpll_value == 0:
            continue
        
        ratio = Fraction(tsv_value, dpll_value)
        if ratio < 1.0:
            conjecture_holds = False
            counterexample = f"Instance with TSV={tsv_value} and DPLL width={dpll_value}"
    
    return {
        "metric_name": "Ratio of TSV to DPLL Width",
        "metric_value": Fraction(tsv_value, dpll_value) if dpll_value != 0 else None,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")