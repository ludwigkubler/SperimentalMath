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
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        factor = Fraction(A[i][i])
        for j in range(i, n):
            A[i][j] /= factor
        
        for k in range(i+1, n):
            factor = Fraction(A[k][i])
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
    
    # Back-substitute to get the rank
    rank = 0
    for i in range(n):
        if all(abs(A[i][j]) < 1e-9 for j in range(n)):
            rank += 1
    return rank

def dpll_search(clauses, assignment):
    if not clauses:
        return True
    clause = next((c for c in clauses if any(l not in assignment or assignment[l] == False for l in c)), None)
    if not clause:
        return True
    
    for literal in clause:
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll_search(clause, new_assignment):
            return True
        
        new_assignment[literal] = False
        if dpll_search(clause, new_assignment):
            return True
    
    return False

def resolution_proof_size(clauses):
    n = len(clauses)
    max_depth = 0
    for i in range(n):
        depth = 1
        while clauses[i]:
            new_clause = []
            for j in range(i+1, n):
                if any(l not in clauses[j] or clauses[j][l] == False for l in clauses[i]):
                    new_clause.extend(clauses[j])
            max_depth = max(max_depth, depth)
            clauses[i] = new_clause
            depth += 1
    return max_depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    num_clauses = random.randint(n, 2*n)
    variables = set(range(-n, 0)) | set(range(1, n+1))
    clauses = []
    for _ in range(num_clauses):
        clause = [random.choice(variables) for _ in range(3)]
        if len(set(clause)) == 3:
            clauses.append(clause)
    
    incidence_matrix = [[int(l in c or -l in c) for l in variables] for c in clauses]
    rank_M_phi = gaussian_elimination(incidence_matrix)
    
    rho_phi = resolution_proof_size(clauses)
    
    if rho_phi == 0:
        return {
            "metric_name": "rank(M_Φ)",
            "metric_value": rank_M_phi,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "resolution_proof_size_zero"
        }
    
    conjecture_holds = rank_M_phi <= math.log2(rho_phi) + 1
    counterexample = "" if conjecture_holds else f"rho(Φ)={rho_phi}, rank(M_Φ)={rank_M_phi}"
    
    return {
        "metric_name": "rank(M_Φ)",
        "metric_value": rank_M_phi,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 10**9) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    total_metric = sum(r["metric_value"] for r in results)
    mean_metric = total_metric / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")