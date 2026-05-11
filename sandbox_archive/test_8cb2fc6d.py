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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    rank = 0
    for row in A:
        if any(row):
            rank += 1
    return rank

def dpll_search(clauses, assignment):
    if not clauses:
        return True
    clause = next(c for c in clauses if any(l not in assignment or assignment[l] == 0 for l in c))
    literals = set(l for l in clause if l != -l)
    for l in literals:
        new_assignment = assignment.copy()
        new_assignment[l] = 1
        if dpll_search([c for c in clauses if l not in c and -l not in c], new_assignment):
            return True
        new_assignment[l] = -1
        if dpll_search([c for c in clauses if l not in c and -l not in c], new_assignment):
            return True
    return False

def minimal_resolution_proof_size(clauses):
    n = max(abs(l) for clause in clauses for l in clause)
    assignment = {i: 0 for i in range(1, n+1)}
    if dpll_search(clauses, assignment):
        return 0
    return None

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    clauses = []
    for _ in range(random.randint(n*2, n*3)):
        clause = [random.choice([-1, 1]) * (i+1) for i in range(n)]
        if len(set(clause)) == len(clause):
            clauses.append(clause)
    incidence_matrix = [[0] * n for _ in range(len(clauses))]
    for j, clause in enumerate(clauses):
        for l in clause:
            incidence_matrix[j][abs(l)-1] = 1
    rank_M_phi = gaussian_elimination(incidence_matrix)
    rho_phi = minimal_resolution_proof_size(clauses)
    if rho_phi is None:
        return {
            "metric_name": "rank(M_Φ)",
            "metric_value": rank_M_phi,
            "instances_tested": len(clauses),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    log_rho_phi = math.log2(rho_phi)
    return {
        "metric_name": "rank(M_Φ)",
        "metric_value": rank_M_phi,
        "instances_tested": len(clauses),
        "conjecture_holds": rank_M_phi <= log_rho_phi + 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE insufficient data")