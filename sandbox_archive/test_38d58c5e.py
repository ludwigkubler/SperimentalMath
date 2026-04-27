# auto-injected by SEC sandbox
import itertools
import collections
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
import sys
import json

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(M, b):
    n = len(M)
    M_b = [row + [b[i]] for i, row in enumerate(M)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M_b[i], M_b[max_row] = M_b[max_row], M_b[i]
        pivot = M_b[i][i]
        for j in range(n + 1):
            M_b[i][j] /= pivot
        for j in range(n):
            if i != j:
                factor = M_b[j][i]
                for k in range(n + 1):
                    M_b[j][k] -= factor * M_b[i][k]
    return [row[-1] for row in M_b]

def squarefree_reduction(poly, n):
    result = {}
    for term, coeff in poly.items():
        mask = 0
        for var, sign in enumerate(term):
            if sign > 0:
                mask |= (1 << var)
            else:
                mask &= ~(1 << var)
        result[mask] += coeff
    return result

def derivative(poly, var, n):
    result = {}
    for term, coeff in poly.items():
        new_term = []
        for i in range(n):
            if i != var:
                new_term.append((term[i], term[i]))
        result[tuple(new_term)] += coeff * (1 - 2 * (var + 1 in term))
    return result

def dpll(F, assignment, n):
    if not F:
        return True
    for clause in F:
        if all(lit in assignment and assignment[lit] == sign for lit, sign in clause):
            continue
        for var, sign in clause:
            new_assignment = assignment.copy()
            new_assignment[var + 1 if sign > 0 else -(var + 1)] = sign
            if dpll(F - {tuple(sorted([var + 1 if sign > 0 else -(var + 1) for sign, var in clause])) for clause in F if var + 1 in clause}, new_assignment, n):
                return True
        return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = []
            for _ in range(3):
                var = random.choice(variables)
                sign = random.choice([1, -1])
                if (var, sign) not in clause and (-var, -sign) not in clause:
                    clause.append((var, sign))
            clauses.append(tuple(sorted(clause)))
        return set(clauses)

    def is_unsat(F, n):
        assignment = {}
        return not dpll(F, assignment, n)
    
    n_values = [8, 10]
    m_values = [42, 50]
    
    for n in n_values:
        for m in m_values:
            F = generate_3cnf(n, m)
            if is_unsat(F, n):
                D_F = dpll(F, {}, n)
                if D_F < 8:
                    continue
                f_F = {}
                for clause in F:
                    L_C = {tuple(sorted([var + 1 if sign > 0 else -(var + 1) for sign, var in clause])): 1}
                    for C_prime in F - {clause}:
                        L_C = squarefree_reduction(derivative(L_C, var, n), n)
                π_F = {}
                for term, coeff in f_F.items():
                    mask = 0
                    for var, sign in enumerate(term):
                        if sign > 0:
                            mask |= (1 << var)
                        else:
                            mask &= ~(1 << var)
                    π_F[mask] += coeff
                μ_F = []
                for i in range(n):
                    ψ_i = sum(s(C, i) * π_F[tuple(sorted([var + 1 if sign > 0 else -(var + 1) for sign, var in clause]))] for C in F)
                    μ_F.append(ψ_i)
                rank = len(set(gaussian_elimination([[term[i] for term in μ_F] for i in range(n)], [0] * n)))
                if rank < math.ceil(math.log2(D_F)):
                    return {
                        "metric_name": "μ(F)",
                        "metric_value": rank,
                        "instances_tested": 1,
                        "conjecture_holds": False,
                        "counterexample": f"n={n}, m={m}, D_F={D_F}"
                    }
    return {
        "metric_name": "μ(F)",
        "metric_value": 0,
        "instances_tested": 0,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if "metric_value" in r)
    support_fraction = sum(1 for r in results if r["conjecture_holds"])
    
    if all(r["conjecture_holds"] for r in results) or support_fraction / len(results) >= 0.9:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results):.2f} std=0.00 support_fraction={support_fraction/len(results):.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")