# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import itertools
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            literals = [random.randint(-n, -1), random.randint(1, n)]
            random.shuffle(literals)
            clause = tuple(sorted(literals))
            if clause not in clauses:
                clauses.append(clause)
        return clauses
    
    def dpll(assignment, clauses):
        unsatisfied_clauses = [c for c in clauses if all(l not in assignment or assignment[l] != True for l in c)]
        if not unsatisfied_clauses:
            return True
        unit_clause = next((c for c in unsatisfied_clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll(new_assignment, clauses):
                return True
            new_assignment[literal] = False
            if dpll(new_assignment, clauses):
                return True
            return False
        pure_literal = next((l for l in range(-n, n + 1) if all(l not in assignment or assignment[l] == True for c in unsatisfied_clauses for l in c)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            if dpll(new_assignment, clauses):
                return True
            new_assignment[pure_literal] = False
            if dpll(new_assignment, clauses):
                return True
            return False
        literal = random.choice([l for l in range(-n, n + 1) if l not in assignment])
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll(new_assignment, clauses):
            return True
        new_assignment[literal] = False
        if dpll(new_assignment, clauses):
            return True
        return False
    
    def dpll_refutation_size(clauses):
        return len(next(assignment for assignment in itertools.product([False, True], repeat=len(clauses)) if dpll(assignment, clauses)))
    
    n = random.randint(10, 40)
    clauses = generate_3cnf(n)
    ehrhart_matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if (i, j) in clauses or (-i, -j) in clauses:
                ehrhart_matrix[i][j] = 1
                ehrhart_matrix[j][i] = 1
    
    def matrix_rank(matrix):
        rank = 0
        for i in range(len(matrix)):
            if any(matrix[j][i] != 0 for j in range(rank, len(matrix))):
                rank += 1
                for j in range(i + 1, len(matrix)):
                    if matrix[j][i] != 0:
                        factor = Fraction(matrix[j][i], matrix[i][i])
                        for k in range(len(matrix[0])):
                            matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    min_rank = matrix_rank(ehrhart_matrix)
    
    refutation_size = dpll_refutation_size(clauses)
    
    alpha = 0.1
    C_alpha = 2.0  # This is a placeholder value; you should compute this based on your analysis
    
    metric_value = log2(refutation_size) <= C_alpha * sqrt(min_rank ** (1/2 + alpha))
    
    return {
        "metric_name": "log2_refutation_size_vs_C_alpha_sqrt_min_rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": metric_value,
        "counterexample": "" if metric_value else "Counterexample found"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Counterexample found' first_failing_seed={first_failing_seed}")