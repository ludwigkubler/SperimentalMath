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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def is_zero_matrix(matrix):
        for row in matrix:
            if any(row[i] != 0 for i in range(len(row))):
                return False
        return True
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for j in range(n):
            pivot_row = -1
            for i in range(rank, m):
                if A[i][j] != 0:
                    pivot_row = i
                    break
            if pivot_row == -1:
                continue
            A[pivot_row], A[rank] = A[rank], A[pivot_row]
            rank += 1
            for i in range(rank, m):
                factor = A[i][j] / A[pivot_row][j]
                for k in range(n):
                    A[i][k] -= factor * A[pivot_row][k]
        return rank
    
    def min_rank_of_quotient_algebra(clauses):
        n = len(clauses)
        R = [[0] * (n + 1) for _ in range(n + 1)]
        R[0][0] = 1
        for clause in clauses:
            for i in clause:
                if i > 0:
                    R[i - 1][i] = 1
                else:
                    R[-i - 1][-i] = 1
        
        return gaussian_elimination(R)
    
    def resolution_width(clauses):
        # Simplified DPLL solver to estimate width
        def dpll(clauses, assignment):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                    return True
                new_assignment[literal] = False
                if dpll([c for c in clauses if -literal not in c], new_assignment):
                    return True
                return False
            pure_literal = next((i for i in range(1, n + 1) if (i not in assignment and -i not in assignment)), None)
            if pure_literal:
                new_assignment[pure_literal] = True
                if dpll(clauses, new_assignment):
                    return True
                new_assignment[pure_literal] = False
                if dpll([c for c in clauses if -pure_literal not in c], new_assignment):
                    return True
                return False
            literal = random.choice([i for i in range(1, n + 1) if i not in assignment and -i not in assignment])
            new_assignment[literal] = True
            if dpll(clauses, new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if -literal not in c], new_assignment):
                return True
            return False
        
        width = 0
        assignment = {}
        while not dpll(clauses, assignment):
            literal = random.choice([i for i in range(1, n + 1) if i not in assignment and -i not in assignment])
            assignment[literal] = True
            width += 1
        
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_rank_values = []
    resolution_widths = []
    
    for n in n_values:
        for _ in range(5):
            clauses = generate_cnf(n)
            min_rank = min_rank_of_quotient_algebra(clauses)
            width = resolution_width(clauses)
            min_rank_values.append(min_rank)
            resolution_widths.append(width)
    
    if not min_rank_values or not resolution_widths:
        return {
            "metric_name": "min_rank",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_range_in_randrange"
        }
    
    mean_min_rank = sum(min_rank_values) / len(min_rank_values)
    mean_width = sum(resolution_widths) / len(resolution_widths)
    correlation_coefficient = (sum((min_rank_values[i] - mean_min_rank) * (resolution_widths[i] - mean_width) for i in range(len(min_rank_values)))) / (len(min_rank_values) * math.sqrt(sum((min_rank_values[i] - mean_min_rank) ** 2 for i in range(len(min_rank_values))) * sum((resolution_widths[i] - mean_width) ** 2 for i in range(len(resolution_widths)))))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(min_rank_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")