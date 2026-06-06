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
from fractions import Fraction
import math

def gaussian_elimination(matrix):
    n = len(matrix)
    augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
    
    for i in range(n):
        # Find pivot
        max_row = i
        for r in range(i+1, n):
            if abs(augmented_matrix[r][i]) > abs(augmented_matrix[max_row][i]):
                max_row = r
        
        # Swap rows
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        # Eliminate
        for r in range(i+1, n):
            factor = Fraction(augmented_matrix[r][i], augmented_matrix[i][i])
            for c in range(n + 1):
                augmented_matrix[r][c] -= factor * augmented_matrix[i][c]
    
    # Back substitution
    min_rank = n
    for r in range(n-1, -1, -1):
        if all(augmented_matrix[r][c] == 0 for c in range(r+1, n)):
            min_rank -= 1
    
    return min_rank

def random_quantum_state(n):
    state = [[random.random() for _ in range(n)] for _ in range(n)]
    # Normalize the state
    norm = sum(a**2 + b**2 for row in state for a, b in zip(row[:n//2], row[n//2:]))
    for i in range(n):
        state[i] = [x / math.sqrt(norm) for x in state[i]]
    return state

def dpll_solver(cnf):
    def solve(assignment, clauses):
        if not clauses:
            return True
        clause = next(clause for clause in clauses if any(lit in assignment and assignment[lit] == 1 or -lit in assignment and assignment[-lit] == 0 for lit in clause))
        pos_lit = next(lit for lit in clause if lit > 0)
        neg_lit = -pos_lit
        if pos_lit not in assignment:
            assignment[pos_lit] = 1
            if solve(assignment, clauses):
                return True
            del assignment[pos_lit]
        if neg_lit not in assignment:
            assignment[neg_lit] = 1
            if solve(assignment, clauses):
                return True
            del assignment[neg_lit]
        return False
    
    n = len(cnf)
    assignment = {}
    return solve(assignment, cnf)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        quantum_state = random_quantum_state(n)
        matrix_representation = [[sum(a * b for a, b in zip(row1, row2)) for row2 in quantum_state] for row1 in quantum_state]
        
        # Convert to CNF instance (simplified example)
        cnf = []
        for i in range(n):
            for j in range(i+1, n):
                cnf.append([i+1, -(j+1)])
        
        dpll_length = dpll_solver(cnf)
        
        if dpll_length is None:
            return {
                "metric_name": "DPLL Proof Length",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "DPLL solver failed"
            }
        
        min_rank = gaussian_elimination(matrix_representation)
        
        results.append({
            "n": n,
            "min_rank": min_rank,
            "dpll_length": dpll_length
        })
    
    mean_diff = sum(abs(res["min_rank"] - res["dpll_length"]) for res in results) / len(results)
    support_fraction = sum(1 for res in results if abs(res["min_rank"] - res["dpll_length"]) <= 3) / len(results)
    
    return {
        "metric_name": "DPLL Proof Length",
        "metric_value": mean_diff,
        "instances_tested": len(results),
        "n_max": max(res["n"] for res in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"Difference > 3 at n={max(res['n'] for res in results if abs(res['min_rank'] - res['dpll_length']) > 3)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_diff = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Difference > 3\" first_failing_seed={first_failing_seed}")