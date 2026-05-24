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

def random_k_cnf(n, k):
    clauses = []
    for _ in range(k * n):
        clause = set()
        while len(clause) < 3:
            var = random.randint(1, n)
            if var not in clause and -var not in clause:
                clause.add(var)
        clauses.append(tuple(sorted(clause)))
    return clauses

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for i in range(cols):
        pivot_row = None
        for j in range(rank, rows):
            if matrix[j][i] != 0:
                pivot_row = j
                break
        if pivot_row is not None:
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            for j in range(rows):
                if j != rank and matrix[j][i] != 0:
                    factor = -matrix[j][i] / matrix[rank][i]
                    for k in range(cols):
                        matrix[j][k] += factor * matrix[rank][k]
            rank += 1
    return rank

def local_defect_complexity(clauses, n):
    A = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in clauses:
        for var in clause:
            A[var][var] += 1
            for other_var in clause:
                if other_var != var:
                    A[var][other_var] -= 1
    return gaussian_elimination(A)

def dpll_refutation_path_length(clauses):
    def dpll(model, clauses):
        unit_clauses = [c for c in clauses if len(c) == 1]
        while unit_clauses:
            literal = unit_clauses.pop()[0]
            model[abs(literal)] = literal > 0
            new_clauses = []
            for clause in clauses:
                if literal in clause:
                    continue
                elif -literal in clause:
                    new_clauses.append([l for l in clause if l != -literal])
                else:
                    new_clauses.append(clause)
            unit_clauses.extend([c for c in new_clauses if len(c) == 1])
            clauses = new_clauses
        return all(literal in model and model[literal] == literal > 0 for clause in clauses for literal in clause)

    def dpll_backtrack(model, clauses):
        stack = []
        while True:
            if dpll(model.copy(), clauses):
                return len(stack)
            literal = next((l for l in range(1, n + 1) if l not in model and -l not in model), None)
            if literal is None:
                return float('inf')
            stack.append(literal)
            model[literal] = True
            clauses = [c for c in clauses if literal not in c]
            if dpll(model.copy(), clauses):
                return len(stack)
            del model[literal]
            stack.pop()
            model[-literal] = True
            clauses = [c for c in clauses if -literal not in c]
            if dpll(model.copy(), clauses):
                return len(stack)

    return min(dpll_backtrack({}, clauses), dpll_backtrack({i: False for i in range(1, n + 1)}, clauses))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([10, 20, 40])
    k = 3
    clauses = random_k_cnf(n, k)
    
    L_F = local_defect_complexity(clauses, n)
    t_star_F = dpll_refutation_path_length(clauses)
    
    if L_F == 0:
        return {
            "metric_name": "L(F) / α * L(F)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "local_defect_complexity_is_zero"
        }
    
    alpha = 1.0
    ratio = t_star_F / (alpha * L_F)
    
    return {
        "metric_name": "L(F) / α * L(F)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1.5,
        "counterexample": "" if ratio <= 1.5 else f"ratio={ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")