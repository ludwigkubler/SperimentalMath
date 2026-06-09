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
    
    def generate_tseitin_formula(n):
        variables = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append([variables[i-1]])
            clauses.append([-variables[i-1]])
        for i in range(1, n):
            for j in range(i+1, n+1):
                clauses.append([variables[i-1], -variables[j-1]])
                clauses.append([-variables[i-1], variables[j-1]])
                clauses.append([variables[i-1], variables[j-1]])
        return clauses
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n-1, i-1, -1):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n-1, i-1, -1):
                        A[k][j] -= factor * A[i][j]
        rank = sum(1 for row in A if any(row[j] != 0 for j in range(n)))
        return rank
    
    def compute_tropical_hodge_structure_rank(clauses):
        n = len(clauses)
        A = [[0]*n for _ in range(n)]
        for clause in clauses:
            for lit in clause:
                i = abs(lit) - 1
                if lit > 0:
                    A[i][i] += 1
                else:
                    A[i][i] -= 1
        return gaussian_elimination(A)
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            lit = unit_clause[0]
            if lit < 0 and -lit in assignment:
                return False
            assignment[lit] = True
            new_clauses = [c for c in clauses if not any(l in c for l in assignment)]
            if dpll(new_clauses, assignment):
                return True
            del assignment[lit]
        else:
            lit = next((i+1 for i in range(n) if i+1 not in assignment and -i-1 not in assignment), None)
            assignment[lit] = True
            new_clauses = [c for c in clauses if not any(l in c for l in assignment)]
            if dpll(new_clauses, assignment):
                return True
            del assignment[lit]
        assignment[-lit] = True
        new_clauses = [c for c in clauses if not any(l in c for l in assignment)]
        if dpll(new_clauses, assignment):
            return True
        del assignment[-lit]
        return False
    
    def resolution_width(clauses):
        n = len(clauses)
        width = 0
        for _ in range(10):  # Run DPLL multiple times to get an average width
            assignment = {}
            if dpll(clauses, assignment):
                width += max(len([l for l in assignment if assignment[l]]) for l in range(-n, n+1))
        return width / 10
    
    def generate_random_clauses(n):
        clauses = []
        for _ in range(2*n):
            clause = [random.choice([-i-1, i+1] for i in range(1, n+1))]
            clauses.append(clause)
        return clauses
    
    n_values = [5, 10, 15, 20, 30, 40]
    circuit_ranks = []
    widths = []
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            clauses = generate_tseitin_formula(n)
            rank = compute_tropical_hodge_structure_rank(clauses)
            width = resolution_width(clauses)
            circuit_ranks.append(rank)
            widths.append(width)
    
    correlation_coefficient = sum((circuit_ranks[i] - sum(circuit_ranks) / len(circuit_ranks)) * (widths[i] - sum(widths) / len(widths)) for i in range(len(circuit_ranks))) / (len(circuit_ranks) * math.sqrt(sum((circuit_ranks[i] - sum(circuit_ranks) / len(circuit_ranks))**2 for i in range(len(circuit_ranks)))) * math.sqrt(sum((widths[i] - sum(widths) / len(widths))**2 for i in range(len(widths)))))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(circuit_ranks),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.8,
        "counterexample": "" if abs(correlation_coefficient) > 0.8 else "correlation_coefficient < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")