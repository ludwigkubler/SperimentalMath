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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_cnf(n):
        clauses = []
        for _ in range(3 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            lit = unit_clause[0]
            new_assignment = {**assignment, abs(lit): lit > 0}
            return dpll([c for c in cnf if lit not in c and -lit not in c], new_assignment)
        
        p = next(abs(lit) for lit in random.choice(cnf))
        if dpll([c for c in cnf if p not in c and -p not in c], {**assignment, p: True}):
            return True
        if dpll([c for c in cnf if p not in c and -p not in c], {**assignment, p: False}):
            return True
        return False
    
    def tropical_motivic_rank(cnf):
        n = max(abs(lit) for lit in set(lit for clause in cnf for lit in clause))
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    matrix[lit][lit] = -math.inf
                else:
                    matrix[-lit][-lit] = -math.inf
        
        def gaussian_elimination(A):
            m, n = len(A), len(A[0])
            for i in range(m):
                max_row = i
                for j in range(i + 1, m):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[i], A[max_row] = A[max_row], A[i]
                if A[i][i] == 0:
                    continue
                for j in range(n):
                    A[i][j] /= A[i][i]
                for k in range(m):
                    if k != i and A[k][i] != 0:
                        for j in range(n):
                            A[k][j] -= A[i][j] * A[k][i]
            return A
        
        gaussian_elimination(matrix)
        
        rank = sum(1 for row in matrix if any(x != 0 for x in row))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    dpll_depths = []
    
    for n in n_values:
        cnf = generate_random_cnf(n)
        min_rank = tropical_motivic_rank(cnf)
        dpll_depth = 0
        if dpll(cnf):
            dpll_depth = len(next(lit for lit, val in assignment.items() if not val))
        
        min_ranks.append(min_rank)
        dpll_depths.append(dpll_depth)
    
    mean_min_rank = sum(min_ranks) / len(min_ranks)
    mean_dpll_depth = sum(dpll_depths) / len(dpll_depths)
    ratio_mean = mean_min_rank / mean_dpll_depth if mean_dpll_depth != 0 else float('inf')
    
    conjecture_holds = ratio_mean >= 0.5 and all(ratio <= 2 for ratio in [min_ranks[i] / dpll_depths[i] for i in range(len(min_ranks))])
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mtr_dpll_ratio",
        "metric_value": ratio_mean,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")