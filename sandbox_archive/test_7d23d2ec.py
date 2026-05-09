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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for k in range(i+1, n):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k
            A[i], A[max_row] = A[max_row], A[i]
            factor = Fraction(A[i][i], 1)
            for j in range(n):
                A[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = Fraction(A[k][i], 1)
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def determinant(A):
        n = len(A)
        det = Fraction(1, 1)
        for i in range(n):
            det *= A[i][i]
        return det
    
    def algebraic_connectivity(G):
        n = len(G)
        L = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j]:
                    L[i][j] = -1
                    L[j][i] = -1
        L[i][i] = sum(G[i]) - 1
        
        L = gaussian_elimination(L)
        det_L = determinant(L)
        
        return abs(det_L) / (2 * n**2)
    
    def generate_tseitin_formula(n):
        literals = [f'x{i+1}' for i in range(n)]
        clauses = []
        for i in range(n):
            clauses.append([literals[i]])
            for j in range(i+1, n):
                clauses.append([-literals[i], -literals[j]])
                clauses.append([literals[i], literals[j]])
        return clauses
    
    def dpll(clauses, assignment, model=[]):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment + [literal] if literal > 0 else assignment + [-literal]
            new_model = model + [(abs(literal), literal)]
            return dpll(clauses, new_assignment, new_model)
        
        literal = next((l for l in literals if l not in assignment and -l not in assignment), None)
        if not literal:
            return False
        
        new_assignment1 = assignment + [literal]
        new_assignment2 = assignment + [-literal]
        return dpll(clauses, new_assignment1) or dpll(clauses, new_assignment2)
    
    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    μ_G = algebraic_connectivity(G)
    if μ_G == 0:
        return {
            "metric_name": "DPLL Tree Size",
            "metric_value": None,
            "instances_tested": n * (n - 1) // 2,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    clauses = generate_tseitin_formula(n)
    dpll_tree_size = 0
    for _ in range(30):
        if dpll(clauses, []):
            dpll_tree_size += 1
    
    return {
        "metric_name": "DPLL Tree Size",
        "metric_value": dpll_tree_size,
        "instances_tested": n * (n - 1) // 2,
        "conjecture_holds": dpll_tree_size >= 2**(0.5 * μ_G),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 10**9) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")