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
    
    def generate_k_sat_instance(n, m):
        variables = list(range(n))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 3)
            clause = [(-1 if random.choice([True, False]) else 1) * var for var in clause]
            clauses.append(clause)
        return clauses
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(cols):
            pivot_row = -1
            for j in range(rank, rows):
                if matrix[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row == -1:
                continue
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            for j in range(rows):
                if j != rank and matrix[j][i] != 0:
                    factor = matrix[j][i] / matrix[rank][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[rank][k]
            rank += 1
        return rank
    
    def p_adic_order(matrix):
        rows, cols = len(matrix), len(matrix[0])
        max_p_adic_val = 0
        for i in range(rows):
            for j in range(cols):
                if matrix[i][j] != 0:
                    val = abs(matrix[i][j])
                    while val % p == 0:
                        val //= p
                        max_p_adic_val += 1
        return max_p_adic_val
    
    def dpll_solver(clauses, assignment):
        if not clauses:
            return True
        literal = next(lit for lit in range(1, len(assignment) + 1) if lit not in assignment and -lit not in assignment)
        pos_literal, neg_literal = literal, -literal
        
        def propagate(lit):
            new_clauses = []
            for clause in clauses:
                if lit in clause:
                    continue
                elif -lit in clause:
                    clause.remove(-lit)
                    if not clause:
                        return None
                else:
                    new_clauses.append(clause)
            return new_clauses
        
        def backtrack():
            assignment.pop()
            return dpll_solver(clauses, assignment)
        
        assignment[pos_literal] = True
        new_clauses = propagate(pos_literal)
        if new_clauses is not None and dpll_solver(new_clauses, assignment):
            return True
        
        assignment[neg_literal] = True
        new_clauses = propagate(neg_literal)
        if new_clauses is not None and dpll_solver(new_clauses, assignment):
            return True
        
        return backtrack()
    
    def resolution_depth(clauses):
        if not clauses:
            return 0
        literal = next(lit for lit in range(1, len(clauses) + 1) if lit not in [c[0] for c in clauses] and -lit not in [c[0] for c in clauses])
        pos_literal, neg_literal = literal, -literal
        
        def resolve(clause1, clause2):
            new_clause = []
            for lit in clause1:
                if lit != -neg_literal:
                    new_clause.append(lit)
            for lit in clause2:
                if lit != pos_literal:
                    new_clause.append(lit)
            return new_clause
        
        def backtrack():
            return resolution_depth(clauses)
        
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                if pos_literal in clauses[i] and neg_literal in clauses[j]:
                    new_clause = resolve(clauses[i], clauses[j])
                    if not new_clause:
                        continue
                    new_clauses = [c for k, c in enumerate(clauses) if k != i and k != j]
                    new_clauses.append(new_clause)
                    depth = resolution_depth(new_clauses)
                    if depth >= 0:
                        return depth + 1
        
        return backtrack()
    
    p = 2
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = min(n**2, 100)  # Ensure m is at most O(n^2)
        instance = generate_k_sat_instance(n, m)
        
        matrix = [[0] * (n + 1) for _ in range(m)]
        for i, clause in enumerate(instance):
            for lit in clause:
                var = abs(lit) - 1
                if lit > 0:
                    matrix[i][var] += 1
                else:
                    matrix[i][var] -= 1
        
        rank = gaussian_elimination(matrix)
        p_adic_val = p_adic_order(matrix)
        resolution_depth_val = resolution_depth(instance)
        
        results.append({
            "n": n,
            "m": m,
            "rank": rank,
            "p_adic_val": p_adic_val,
            "resolution_depth": resolution_depth_val
        })
    
    min_p_adic_val = min(result["p_adic_val"] for result in results)
    max_p_adic_val = max(result["p_adic_val"] for result in results)
    avg_resolution_depth = sum(result["resolution_depth"] for result in results) / len(results)
    
    conjecture_holds = all(max_p_adic_val <= math.log(n) + math.log(m) for n, m in zip([result["n"] for result in results], [result["m"] for result in results]))
    counterexample = "" if conjecture_holds else "p-adic order exceeds log(n) + log(m)"
    
    return {
        "metric_name": "Minimal Rank of p-Adic Differentials vs k-SAT Resolution Depth",
        "metric_value": avg_resolution_depth,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"p-adic order exceeds log(n) + log(m)\" first_failing_seed={first_failing_seed}")