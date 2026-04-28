# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import sys
from itertools import combinations

def lex_dpll(F, unit_propagate=True):
    assignment = {}
    stack = []
    for clause in F:
        if all(lit in assignment and not assignment[lit] for lit in clause):
            return None  # UNSAT
        if any(lit in assignment and assignment[lit] for lit in clause):
            continue
        unit_clauses = [lit for lit in clause if lit not in assignment and -lit not in assignment]
        if unit_clauses:
            stack.append((unit_clauses, assignment.copy()))
            assignment[unit_clauses[0]] = True
    while stack:
        unit_clauses, current_assignment = stack.pop()
        new_clause = [lit for lit in unit_clauses if lit not in current_assignment and -lit not in current_assignment]
        if new_clause:
            stack.append((new_clause, current_assignment.copy()))
            current_assignment[new_clause[0]] = True
        else:
            assignment.update(current_assignment)
    return assignment

def r2(F):
    rounds = 0
    while True:
        new_F = []
        for clause in F:
            if any(lit not in assignment and -lit not in assignment for lit in clause):
                new_F.append([lit for lit in clause if lit in assignment or -lit in assignment])
        if len(new_F) == len(F):
            return rounds
        F = new_F
        rounds += 1
    return math.inf

def generate_formula(n, alpha):
    variables = list(range(1, n + 1))
    clauses = []
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            clauses.append([i, j])
    for clause in combinations(variables, int(alpha * n)):
        clauses.append(list(clause))
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [6, 8, 10, 12]
    alpha_values = [4.5, 5.0, 6.0]
    results = []
    
    for n in n_values:
        for alpha in alpha_values:
            for _ in range(80):
                F = generate_formula(n, alpha)
                if lex_dpll(F) is None:
                    continue
                r2_value = r2(F)
                L_value = len(lex_dpll(F))
                results.append((r2_value, L_value, n))
    
    metric_name = "log2_L_over_r2_plus_log2_n"
    instances_tested = len(results)
    conjecture_holds = True
    counterexample = ""
    
    for r2_value, L_value, n in results:
        if r2_value < math.inf and not (math.log2(L_value) <= 2 * r2_value + 2 * math.log2(n + 1)):
            conjecture_holds = False
            counterexample = f"r2={r2_value}, L={L_value}, n={n}"
        if r2_value == math.inf and not (math.log2(L_value) >= n / 4):
            conjecture_holds = False
            counterexample = f"r2=∞, L={L_value}, n={n}"
    
    metric_value = sum(math.log2(L) / (2 * r + 2 * math.log2(n + 1)) if r < math.inf else math.log2(L) >= n / 4 for r, L, n in results)
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")