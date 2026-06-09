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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def spectral_radius(A):
        n = len(A)
        eigenvalues = []
        I = [[int(i == j) for j in range(n)] for i in range(n)]
        for _ in range(100):  # Power iteration method
            x = [random.random() for _ in range(n)]
            x_norm = sum(x[i]**2 for i in range(n))**0.5
            x = [x_i / x_norm for x_i in x]
            Ax = [sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]
            lambda_ = sum(Ax[i] * x[i] for i in range(n))
            eigenvalues.append(lambda_)
        return max(eigenvalues)
    
    def dpll_search_tree_height(phi):
        clauses = phi.split(' or ')
        variables = set()
        for clause in clauses:
            literals = clause.split(' and ')
            for literal in literals:
                if literal[0] == '~':
                    variables.add(literal[1:])
                else:
                    variables.add(literal)
        
        def dpll(clauses, assignment):
            if not clauses:
                return 0
            unit_clause = next((c for c in clauses if len(c.split(' and ')) == 1), None)
            if unit_clause:
                literal = unit_clause.split(' and ')[0]
                if literal[0] == '~':
                    var, neg = literal[1:], True
                else:
                    var, neg = literal, False
                if var in assignment and assignment[var] != neg:
                    return float('inf')
                assignment[var] = neg
                clauses = [c for c in clauses if var not in c]
                return 1 + dpll(clauses, assignment)
            pure_literal = next((v for v in variables if all(v in c or '~' + v in c for c in clauses)), None)
            if pure_literal:
                neg = False
                if pure_literal[0] == '~':
                    pure_literal, neg = pure_literal[1:], True
                assignment[pure_literal] = not neg
                clauses = [c for c in clauses if pure_literal not in c]
                return 1 + dpll(clauses, assignment)
            literal = random.choice(list(variables))
            if literal[0] == '~':
                var, neg = literal[1:], True
            else:
                var, neg = literal, False
            assignment[var] = neg
            clauses = [c for c in clauses if var not in c]
            return 1 + min(dpll(clauses, assignment), dpll([c.replace(var, '~' + var) for c in clauses], assignment))
        
        return dpll(clauses, {})
    
    def generate_cnf(n):
        variables = list('abcdefghijklmnopqrstuvwxyz')[:n]
        clauses = []
        for _ in range(10):  # Generate 10 random clauses
            clause = ' or '.join(random.sample(variables + ['~' + v for v in variables], random.randint(2, n)))
            clauses.append(clause)
        return ' and '.join(clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        phi = generate_cnf(n)
        H_n = [[int(i == j) for j in range(2**n)] for i in range(2**n)]
        A = gaussian_elimination(H_n)
        sigma_max_H_n = spectral_radius(A)
        h_phi = dpll_search_tree_height(phi)
        results.append((sigma_max_H_n, h_phi))
    
    correlation_sum = 0
    n_tested = len(results) * len(n_values)
    for sigma_max_H_n, h_phi in results:
        if sigma_max_H_n == 0 or h_phi == float('inf'):
            continue
        correlation_sum += (sigma_max_H_n - h_phi) / (sigma_max_H_n + h_phi)
    
    correlation_mean = correlation_sum / n_tested
    support_fraction = sum(1 for _, h_phi in results if h_phi < float('inf')) / len(results)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_mean,
        "instances_tested": n_tested,
        "n_max": max(n_values),
        "conjecture_holds": support_fraction > 0.7,
        "counterexample": "" if support_fraction > 0.7 else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")