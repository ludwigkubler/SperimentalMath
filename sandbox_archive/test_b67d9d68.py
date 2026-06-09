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
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def schur_multiplier(G):
        n = len(G)
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j] == 1:
                    M[i][j] = -1
                    M[j][i] = -1
        return gaussian_elimination(M)

    def frege_proof_width(G):
        n = len(G)
        clauses = []
        for i in range(n):
            clause = [random.choice([-1, 1]) * (j + 1) for j in range(n)]
            clauses.append(clause)
        # Simplified DPLL solver
        def dpll(clauses, assignment):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                if literal > 0 and literal in assignment or literal < 0 and -literal not in assignment:
                    return dpll(clauses, assignment | {literal})
                else:
                    return False
            literal = random.choice([c for c in clauses[0] if c != 0])
            return dpll(clauses, assignment | {literal}) or dpll(clauses, assignment | {-literal})
        return len(clauses) if dpll(clauses, set()) else float('inf')

    def tseitin_formula(G):
        n = len(G)
        num_vars = n * (n - 1) // 2
        clauses = []
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j] == 1:
                    var = (i + 1) * (n - i) // 2 + j - i - 1
                    clauses.append([var])
                    clauses.append([-var, -(i + 1)])
                    clauses.append([-var, -(j + 1)])
        return clauses

    def group_cohomological_dimension(G):
        M = schur_multiplier(G)
        rank = sum(1 for row in M if any(x != 0 for x in row))
        return rank

    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
        for j in range(i+1, n):
            G[j][i] = G[i][j]

    gamma_G = group_cohomological_dimension(G)
    phi_G = tseitin_formula(G)
    f_phi_G = frege_proof_width(phi_G)

    return {
        "metric_name": "group_cohomological_dimension",
        "metric_value": gamma_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": gamma_G <= 3 * f_phi_G and gamma_G >= 0.8 * f_phi_G,
        "counterexample": "" if gamma_G <= 3 * f_phi_G and gamma_G >= 0.8 * f_phi_G else f"gamma(G) = {gamma_G}, f(φ_G) = {f_phi_G}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] != "" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")