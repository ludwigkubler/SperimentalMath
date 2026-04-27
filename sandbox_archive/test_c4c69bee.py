# auto-injected by SEC sandbox
import math
import itertools
import json
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
from collections import defaultdict

def gaussian_elimination(matrix):
    n = len(matrix)
    rank = 0
    for i in range(n):
        if matrix[i][i] == 0:
            found_nonzero = False
            for j in range(i + 1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    found_nonzero = True
                    break
            if not found_nonzero:
                continue
        pivot = matrix[i][i]
        for j in range(i + 1, n):
            factor = matrix[j][i] / pivot
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
        rank += 1
    return rank

def squarefree_reduction(poly):
    result = defaultdict(int)
    for term, coeff in poly.items():
        mask = 0
        for var in range(len(term)):
            if term[var]:
                mask |= (1 << var)
        result[mask] += coeff
    return result

def multiply_polynomials(p1, p2):
    result = defaultdict(int)
    for term1, coeff1 in p1.items():
        for term2, coeff2 in p2.items():
            new_term = tuple(term1[i] ^ term2[i] for i in range(len(term1)))
            result[new_term] += coeff1 * coeff2
    return squarefree_reduction(result)

def compute_f_minus_C(F, C):
    F_minus_C = defaultdict(int)
    for term, coeff in F.items():
        if all(not (term[var] and C[var]) for var in range(len(term))):
            F_minus_C[term] += coeff
    return F_minus_C

def compute_mu(F, n):
    m = len(F)
    psi = [0] * n
    for i in range(n):
        s = 1 if any(C[i] for C in F) else -1
        F_minus_C = F.copy()
        for C in F:
            if not (C[i] or not C[i]):
                F_minus_C[C] *= s
        psi[i] = sum(F_minus_C.values())
    matrix = [[psi[i] & (1 << j) for j in range(n)] for i in range(n)]
    return gaussian_elimination(matrix)

def dpll(F, assignment):
    if not F:
        return True
    var = min((i for i, _ in enumerate(assignment) if assignment[i] is None), default=None)
    if var is None:
        return False
    for val in [0, 1]:
        new_assignment = list(assignment)
        new_assignment[var] = val
        if dpll(F, new_assignment):
            return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if not any(clause):
                clause[random.randint(0, n - 1)] *= -1
            clauses.append(tuple(sorted(clause)))
        return set(clauses)
    
    def off(C):
        return sum(1 for x in C if x < 0)
    
    def compute_f_F(F, n):
        f_F = defaultdict(int)
        for clause in F:
            L_C = off(clause) + sum(x for x in clause if x > 0) - sum(-x for x in clause if x < 0)
            f_F[tuple(sorted(clause))] = L_C
        return f_F
    
    n_values = [8, 10]
    m_values = [42, 50]
    
    for n, m in zip(n_values, m_values):
        F = generate_3cnf(n, m)
        if not dpll(F, [None] * n):
            f_F = compute_f_F(F, n)
            mu_F = compute_mu(f_F, n)
            D_F = 0
            assignment = [None] * n
            stack = [(F, assignment)]
            while stack:
                F, assignment = stack.pop()
                if not F:
                    D_F += 1
                    continue
                var = min((i for i, a in enumerate(assignment) if a is None), default=None)
                if var is None:
                    break
                for val in [0, 1]:
                    new_assignment = list(assignment)
                    new_assignment[var] = val
                    stack.append((F - {tuple(sorted([var + 1 if sign > 0 else -(var + 1) for sign, var in clause])) for clause in F if var + 1 in clause}, new_assignment))
            if mu_F < (D_F.bit_length() - 1):
                return {
                    "metric_name": "mu(F)",
                    "metric_value": mu_F,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, m={m}, D_F={D_F}, mu(F)={mu_F}"
                }
    return {
        "metric_name": "mu(F)",
        "metric_value": None,
        "instances_tested": 0,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["instances_tested"] > 0) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] != "mapping_undefined" for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")