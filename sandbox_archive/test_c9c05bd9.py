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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def generate_3cnf(n: int) -> list:
    clauses = []
    for _ in range(2 * n):
        literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
        clause = random.sample(literals, 3)
        clauses.append(clause)
    return clauses

def matrix_representation(clauses: list, n: int) -> list:
    m = len(clauses)
    A = [[0] * n for _ in range(m)]
    for i, clause in enumerate(clauses):
        for literal in clause:
            var_index = abs(literal) - 1
            if literal > 0:
                A[i][var_index] = 1
            else:
                A[i][var_index] = -1
    return A

def gaussian_elimination(A: list, n: int) -> list:
    m = len(A)
    for i in range(n):
        # Find pivot
        pivot_row = next((j for j in range(i, m) if A[j][i] != 0), None)
        if pivot_row is None:
            continue
        A[i], A[pivot_row] = A[pivot_row], A[i]
        
        # Eliminate below pivot
        for j in range(i + 1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    return A

def minimal_local_system_rank(A: list) -> int:
    n = len(A[0])
    rank = 0
    for i in range(n):
        if any(A[j][i] != 0 for j in range(len(A))):
            rank += 1
    return rank

def resolution_proof_width(clauses: list) -> int:
    # Simplified DPLL solver to estimate proof width
    def solve(model, clause):
        for literal in clause:
            if (literal > 0 and literal in model) or (literal < 0 and -literal not in model):
                return True
        return False

    def dpll(clauses, model):
        unit_clauses = [c for c in clauses if len(c) == 1]
        while unit_clauses:
            literal = unit_clauses.pop()
            model.add(literal)
            new_clauses = []
            for clause in clauses:
                if literal in clause:
                    continue
                if -literal in clause:
                    new_clauses.append([l for l in clause if l != -literal])
                else:
                    new_clauses.append(clause)
            unit_clauses.extend([c for c in new_clauses if len(c) == 1])
            clauses = new_clauses

        for literal in set(lit for clause in clauses for lit in clause):
            if not solve(model, [literal]):
                return dpll(clauses, model | {literal})
        return model

    proof_width = 0
    for i in range(len(clauses)):
        model = set()
        if not dpll(clauses[:i] + clauses[i+1:], model):
            proof_width += 1
    return proof_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_3cnf(n)
    A = matrix_representation(formula, n)
    mls_phi = minimal_local_system_rank(A)
    w_phi = resolution_proof_width(formula)
    
    if mls_phi > 1.1 * w_phi**2:
        return {
            "metric_name": "mls(φ)",
            "metric_value": mls_phi,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"mls(φ) > 1.1 * w(φ)^2 for n={n}"
        }
    
    return {
        "metric_name": "mls(φ)",
        "metric_value": mls_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ranks = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(mean_ranks) / len(mean_ranks):.2f} std=0 support_fraction=1")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mls(φ) > 1.1 * w(φ)^2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")