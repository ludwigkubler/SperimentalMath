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
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def spectral_radius(A):
        n = len(A)
        eigenvalues = [1.0] * n
        for _ in range(100):  # Power iteration method
            v = [random.random() for _ in range(n)]
            v = [x / sum(v) for x in v]
            Av = [sum(a * v[j] for j, a in enumerate(row)) for row in A]
            lambda_new = max(abs(x) for x in Av)
            if abs(lambda_new - eigenvalues[-1]) < 1e-6:
                break
            eigenvalues.append(lambda_new)
        return eigenvalues[-1]

    def dpll_search_tree_height(phi):
        # Simplified DPLL solver to estimate the search tree height
        clauses = phi.split(' or ')
        variables = set()
        for clause in clauses:
            for var in clause.split(' and '):
                if var.startswith('~'):
                    variables.add(var[1:])
                else:
                    variables.add(var)
        
        def dpll(clauses, assignment):
            if not clauses:
                return 0
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                var = unit_clause[0]
                new_assignment = assignment.copy()
                new_assignment[var] = True
                return dpll([c for c in clauses if var not in c], new_assignment)
            
            literal = next((v for v in variables if v not in assignment), None)
            new_assignment_true = assignment.copy()
            new_assignment_true[literal] = True
            height_true = 1 + dpll(clauses, new_assignment_true)
            new_assignment_false = assignment.copy()
            new_assignment_false[literal] = False
            height_false = 1 + dpll(clauses, new_assignment_false)
            return max(height_true, height_false)
        
        return dpll(clauses, {})

    def generate_cnf(n):
        clauses = []
        for i in range(2**n):
            clause = []
            for j in range(n):
                if (i >> j) & 1:
                    clause.append(f'x{j+1}')
                else:
                    clause.append(f'~x{j+1}')
            clauses.append(' or '.join(clause))
        return ' and '.join(clauses)

    n = random.choice([5, 10, 15, 20, 30, 40])
    phi = generate_cnf(n)
    A = [[int(phi[i][j] == 'x' or phi[j][i] == 'x') for j in range(n)] for i in range(n)]
    
    sigma_max = spectral_radius(A)
    h_phi = dpll_search_tree_height(phi)
    
    return {
        "metric_name": "correlation",
        "metric_value": sigma_max * h_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False if sigma_max * h_phi < 0.3 else True,
        "counterexample": "" if sigma_max * h_phi > 0.3 else "correlation_too_low"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] == "correlation_too_low" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] == "correlation_too_low")
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")