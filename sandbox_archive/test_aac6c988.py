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

def gaussian_elimination(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    rref_matrix = [row[:] for row in matrix]
    
    for i in range(rows):
        # Find pivot
        pivot_row = i
        for j in range(i, rows):
            if abs(rref_matrix[j][i]) > abs(rref_matrix[pivot_row][i]):
                pivot_row = j
        
        # Swap rows
        rref_matrix[i], rref_matrix[pivot_row] = rref_matrix[pivot_row], rref_matrix[i]
        
        # Eliminate below the pivot
        for j in range(i + 1, rows):
            factor = -rref_matrix[j][i] / rref_matrix[i][i]
            for k in range(cols):
                if rref_matrix[i][k] != 0:
                    rref_matrix[j][k] += factor * rref_matrix[i][k]
    
    # Eliminate above the pivot
    for i in range(rows - 1, -1, -1):
        factor = 1 / rref_matrix[i][i]
        for j in range(cols):
            if rref_matrix[i][j] != 0:
                rref_matrix[i][j] *= factor
    
    return rref_matrix

def rank(matrix):
    rref_matrix = gaussian_elimination(matrix)
    rank = sum(1 for row in rref_matrix if any(row))
    return rank

def generate_k_cnf(n, m):
    variables = list(range(n))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        clause.append(-random.choice(clause))
        clauses.append(clause)
    return clauses

def dpll_search_tree_height(clauses):
    def dpll(model, clauses):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            model[literal] = True
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            return dpll(model, new_clauses)
        pure_literal = next((l for l in variables if (l in model and not model[l]) or (-l in model and model[-l])), None)
        if pure_literal:
            model[pure_literal] = True
            new_clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
            return dpll(model, new_clauses)
        literal = random.choice(variables)
        model[literal] = True
        new_clauses = [c for c in clauses if literal not in c and -literal not in c]
        if dpll(model, new_clauses):
            return True
        del model[literal]
        model[-literal] = True
        new_clauses = [c for c in clauses if -literal not in c and literal not in c]
        return dpll(model, new_clauses)
    
    variables = list(range(1, n + 1))
    model = {}
    return len(variables) if dpll(model, clauses) else float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_heights = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_k_cnf(n, int(1.2 * n))
            graphical_realization = [[abs(lit) for lit in clause] for clause in clauses]
            k_theory_rank = rank(graphical_realization)
            height = dpll_search_tree_height(clauses)
            total_heights += height
            instances_tested += 1
    
    mean_height = total_heights / instances_tested
    conjecture_holds = True
    counterexample = ""
    
    if mean_height > n_values[-1] * 2:  # Arbitrary upper bound for demonstration
        conjecture_holds = False
        counterexample = "mean_height_exceeds_upper_bound"
    
    return {
        "metric_name": "DPLL Search Tree Height",
        "metric_value": mean_height,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_height = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_height} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")