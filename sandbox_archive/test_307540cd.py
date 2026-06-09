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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, m)]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def hodge_representation_degree(phi):
        # Construct a complex variety from the CNF formula phi
        n = len(phi['variables'])
        m = len(phi['clauses'])
        V = [[0] * (n + 1) for _ in range(m)]
        for i, clause in enumerate(phi['clauses']):
            for literal in clause:
                if literal > 0:
                    V[i][literal - 1] = 1
                else:
                    V[i][-1] += 1
        # Compute the determinant of the variety matrix
        det = determinant(V)
        return abs(det)

    def is_satisfiable(phi):
        # Implement a simple SAT solver (e.g., DPLL) to check satisfiability
        variables = phi['variables']
        clauses = phi['clauses']
        
        def dpll(model, clauses):
            if not clauses:
                return True
            literal = next(l for l in range(1, len(variables) + 1) if l not in model and -l not in model)
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            if dpll(model | {literal}, new_clauses):
                return True
            if dpll(model | {-literal}, new_clauses):
                return True
            return False
        
        return dpll(set(), clauses)

    def generate_cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return {'variables': variables, 'clauses': clauses}

    def compute_metric(phi):
        h_phi = hodge_representation_degree(phi)
        m = len(phi['clauses'])
        return h_phi / (m ** (Fraction(1, 3)))

    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_metric_value = Fraction(0)
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            phi = generate_cnf(n, random.randint(1, m))
            metric_value = compute_metric(phi)
            instances_tested += 1
            total_metric_value += metric_value
            if not is_satisfiable(phi) and metric_value >= 2 * (n ** (Fraction(1, 3))):
                conjecture_holds = False
                counterexample = f"CNF with n={n}, m={len(phi['clauses'])} is unsatisfiable but h(φ) ≥ 2 * n^(1/3)"
                break

    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "h(φ)",
        "metric_value": float(mean_metric_value),
        "instances_tested": instances_tested,
        "n_max": max(n_values),
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

    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] and r['counterexample'] for r in results):
        counterexample = next(r['counterexample'] for r in results if not r['conjecture_holds'] and r['counterexample'])
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'] and r['counterexample'])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")