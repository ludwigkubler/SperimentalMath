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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_symmetric_matrix(n):
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                A[i][j] = random.randint(0, 1)
                A[j][i] = A[i][j]
        return A
    
    def matrix_to_sat(A):
        m, n = len(A), len(A[0])
        clauses = []
        for i in range(m):
            for j in range(n):
                if A[i][j]:
                    clauses.append([1 + 2 * (i * n + j)])
        return clauses
    
    def dpll(clauses, assignment, model):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment[:]
            new_model = model.copy()
            new_model[literal] = literal > 0
            if not dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment, new_model):
                new_model[literal] = not new_model[literal]
                return dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment, new_model)
            return True
        p = next((i for i in range(1, 2 * m * n + 1) if i not in assignment), None)
        if p is None:
            return False
        new_assignment = assignment[:]
        new_assignment.append(p)
        new_model = model.copy()
        new_model[p] = True
        if dpll(clauses, new_assignment, new_model):
            return True
        new_assignment.pop()
        new_model[p] = False
        if dpll(clauses, new_assignment, new_model):
            return True
        return False
    
    def symplectic_rank(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(m):
            for j in range(n):
                if A[i][j]:
                    row = [A[k][j] for k in range(m)]
                    col = [A[i][k] for k in range(n)]
                    if all(row[k] == 0 and col[k] == 0 for k in range(m)):
                        rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            A = generate_symmetric_matrix(n)
            clauses = matrix_to_sat(A)
            h_A = dpll(clauses, [], {})
            κ_L_A = symplectic_rank(A)
            if h_A == 0 or κ_L_A == 0:
                continue
            results.append((κ_L_A, h_A))
    
    if not results:
        return {
            "metric_name": "Ratio of Symplectic Rank to DPLL Height",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    ratio_sum = sum(κ / h for κ, h in results)
    mean_ratio = Fraction(ratio_sum, len(results))
    if mean_ratio > 1.05:
        return {
            "metric_name": "Ratio of Symplectic Rank to DPLL Height",
            "metric_value": float(mean_ratio),
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"Mean ratio {mean_ratio} > 1.05"
        }
    
    return {
        "metric_name": "Ratio of Symplectic Rank to DPLL Height",
        "metric_value": float(mean_ratio),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3**j for i in range(5) for j in range(5)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        if not trial_result["conjecture_holds"]:
            break
        results.append(trial_result["metric_value"])
    
    if len(results) == len(seeds):
        mean = sum(results) / len(results)
        std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
        support_fraction = len([r for r in results if r <= 1.05]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = seeds[results.index(max(results))]
        print(f"RESULT: FALSIFIED counterexample=\"Mean ratio exceeded 1.05\" first_failing_seed={first_failing_seed}")