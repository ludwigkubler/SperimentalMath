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

def generate_cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = set()
        while len(clause) < 2:
            var = random.choice(variables)
            if var not in clause and -var not in clause:
                clause.add(var)
        clauses.append(tuple(sorted(clause)))
    return clauses

def quiver_representation(clauses):
    n = len(clauses)
    Q = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if any(x == y or x == -y for x in clauses[i]) and any(x == y or x == -y for x in clauses[j]):
                Q[i][j] = 1
                Q[j][i] = 1
    return Q

def min_order(Q):
    n = len(Q)
    visited = [False] * n
    order = 0
    
    def dfs(node, current_order):
        if visited[node]:
            return
        visited[node] = True
        for neighbor in range(n):
            if Q[node][neighbor] == 1:
                dfs(neighbor, current_order + 1)
        nonlocal order
        order = max(order, current_order)
    
    for i in range(n):
        if not visited[i]:
            dfs(i, 0)
    
    return order

def dpll_proof_path_length(clauses):
    def dpll(clause_set, assignment):
        if len(clause_set) == 0:
            return True
        unit_clause = next((c for c in clause_set if len(c) == 1), None)
        if unit_clause is not None:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll(clause_set - {unit_clause}, new_assignment):
                return True
            new_assignment[literal] = False
            if dpll(clause_set - {unit_clause, (-literal,)}, new_assignment):
                return True
            return False
        pure_literal = next((l for l in range(1, max(clauses) + 1) if all(l not in c or -l in c for c in clause_set)), None)
        if pure_literal is not None:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            if dpll(clause_set, new_assignment):
                return True
            new_assignment[pure_literal] = False
            if dpll(clause_set - {(-pure_literal,)}, new_assignment):
                return True
            return False
        literal = random.choice(list(assignment.keys()))
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll(clause_set, new_assignment):
            return True
        new_assignment[literal] = False
        if dpll(clause_set - {(-literal,)}, new_assignment):
            return True
        return False
    
    assignment = {}
    for clause in clauses:
        for literal in clause:
            if literal not in assignment:
                assignment[literal] = False
    return len(assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = max(1, int(n * (n - 1) / 4))  # Ensure at least one clause
        clauses = generate_cnf(n, m)
        Q = quiver_representation(clauses)
        min_order_Q = min_order(Q)
        l_phi = dpll_proof_path_length(clauses)
        
        if min_order_Q == 0:
            return {
                "metric_name": "log(min_order(Q(φ)))",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "min_order(Q(φ)) is zero"
            }
        
        results.append({
            "log_min_order_Q": math.log(min_order_Q),
            "l_phi": l_phi
        })
    
    log_min_order_Q_mean = sum(result["log_min_order_Q"] for result in results) / len(results)
    l_phi_mean = sum(result["l_phi"] for result in results) / len(results)
    correlation_coefficient = 0
    
    if len(results) > 1:
        numerator = sum((result["log_min_order_Q"] - log_min_order_Q_mean) * (result["l_phi"] - l_phi_mean) for result in results)
        denominator = math.sqrt(sum((result["log_min_order_Q"] - log_min_order_Q_mean) ** 2 for result in results)) * math.sqrt(sum((result["l_phi"] - l_phi_mean) ** 2 for result in results))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "log(min_order(Q(φ)))",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
    
    results = [run_trial(seed) for seed in seeds]
    correlation_coefficients = [result["metric_value"] for result in results if result["metric_value"] is not None]
    
    if len(correlation_coefficients) >= 25 and all(coef >= 0.7 for coef in correlation_coefficients):
        print(f"RESULT: SUPPORTED mean={sum(correlation_coefficients)/len(correlation_coefficients)} std={math.sqrt(sum((coef - sum(correlation_coefficients)/len(correlation_coefficients))**2 for coef in correlation_coefficients) / len(correlation_coefficients))} support_fraction=1.0")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] is not None and result["metric_value"] < 0.7)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")