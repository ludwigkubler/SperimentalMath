# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def generate_3cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(clause[i] == -clause[j] for i in range(n) for j in range(i + 1, n)):
            continue
        clauses.append(clause)
    return clauses

def dpll_refutation_tree_width(formula):
    def dpll(clauses, assignment):
        if not clauses:
            return 0
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            return max(dpll(new_clauses, new_assignment), dpll(new_clauses, {**new_assignment, literal: False}))
        pure_literal = next((l for l in range(1, 2 * n + 1) if (all(l in c or -l in c for c in clauses)) and not any(-l in c for c in clauses)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            new_clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
            return max(dpll(new_clauses, new_assignment), dpll(new_clauses, {**new_assignment, pure_literal: False}))
        literals = [l for l in range(1, 2 * n + 1) if any(l in c or -l in c for c in clauses)]
        literal = random.choice(literals)
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        new_clauses = [c for c in clauses if literal not in c and -literal not in c]
        return max(dpll(new_clauses, new_assignment), dpll(new_clauses, {**new_assignment, literal: False}))
    return dpll(formula, {})

def tropical_theta_rank(formula):
    n = len(formula[0])
    matrix = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    for clause in formula:
        max_row = None
        max_val = -math.inf
        for i, row in enumerate(matrix):
            val = sum(row[abs(lit) - 1] * (1 if lit > 0 else -1) for lit in clause)
            if val > max_val:
                max_val = val
                max_row = i
        if max_row is not None:
            factor = matrix[max_row][max_row]
            for j in range(n):
                matrix[j][max_row] /= factor
            for i, row in enumerate(matrix):
                if i != max_row:
                    factor = matrix[i][max_row]
                    for j in range(n):
                        matrix[i][j] -= factor * row[max_row]
    rank = sum(1 for row in matrix if any(val != Fraction(0) for val in row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 20, 40]
    results = []
    
    for n in n_values:
        formula = generate_3cnf(n)
        theta_rank = tropical_theta_rank(formula)
        refutation_width = dpll_refutation_tree_width(formula)
        results.append({
            "n": n,
            "theta_rank": theta_rank,
            "refutation_width": refutation_width
        })
    
    mean_theta_rank = sum(result["theta_rank"] for result in results) / len(results)
    std_theta_rank = math.sqrt(sum((result["theta_rank"] - mean_theta_rank) ** 2 for result in results) / len(results))
    correlation = sum((result["theta_rank"] - mean_theta_rank) * (result["refutation_width"] - sum(result["refutation_width"] for result in results) / len(results)) for result in results) / (len(results) * std_theta_rank)
    
    conjecture_holds = correlation < 0
    counterexample = "" if conjecture_holds else "High correlation between theta rank and refutation width"
    
    return {
        "metric_name": "Correlation between tropical theta rank and DPLL refutation tree width",
        "metric_value": correlation,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(seed) for seed in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_correlation = sum(result["metric_value"] for result in results) / len(results)
    std_correlation = math.sqrt(sum((result["metric_value"] - mean_correlation) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_correlation} std={std_correlation} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_correlation} std={std_correlation} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='High correlation between theta rank and refutation width' first_failing_seed={first_failing_seed}")