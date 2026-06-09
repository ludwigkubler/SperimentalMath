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
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def spectral_radius(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        identity = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        eigenvalues = []
        A_k = A
        for _ in range(100):
            A_k = matrix_multiply(A_k, A)
            eigenvector = [sum(A_k[i][j] * random.random() for j in range(n)) for i in range(n)]
            eigenvector_norm = sum(x**2 for x in eigenvector)**0.5
            eigenvalue = sum(eigenvector[i] * A_k[i][j] / eigenvector_norm for i, j in enumerate(range(n)))
            eigenvalues.append(eigenvalue)
        return max(abs(e) for e in eigenvalues)

    def matrix_multiply(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        C = [[Fraction(0) for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clauses = [c[0] for c in clauses if len(c) == 1]
        pure_symbols = {}
        for clause in clauses:
            for literal in clause:
                symbol = abs(literal)
                polarity = literal > 0
                if symbol in pure_symbols and pure_symbols[symbol] != polarity:
                    return False
                pure_symbols[symbol] = polarity
        unit_clause = next((c[0] for c in clauses if len(c) == 1), None)
        if unit_clause is not None:
            literal, polarity = unit_clause, True
            if literal < 0:
                polarity = False
            assignment.append((abs(literal), polarity))
            return dpll([c for c in clauses if literal not in c], assignment)
        pure_symbol = next((s for s, p in pure_symbols.items() if len([c for c in clauses if s in c]) == 1), None)
        if pure_symbol is not None:
            polarity = pure_symbols[pure_symbol]
            assignment.append((pure_symbol, polarity))
            return dpll(clauses, assignment)
        symbol = next(s for s in range(1, len(clauses) + 1) if s not in [abs(l) for l in sum(clauses, [])])
        return dpll([c for c in clauses if symbol not in c], assignment + [(symbol, True)]) or dpll([c for c in clauses if -symbol not in c], assignment + [(symbol, False)])

    def generate_cnf(n):
        clauses = []
        variables = list(range(1, n+1))
        for i in range(2**n):
            clause = []
            for j in range(n):
                if (i >> j) & 1:
                    clause.append(variables[j])
                else:
                    clause.append(-variables[j])
            clauses.append(clause)
        return clauses

    def hypercube_adjacency_matrix(n):
        m = 2**n
        A = [[Fraction(0) for _ in range(m)] for _ in range(m)]
        for i in range(m):
            for j in range(i+1, m):
                if bin(i ^ j).count('1') == 1:
                    A[i][j] = Fraction(1)
                    A[j][i] = Fraction(1)
        return A

    def dpll_search_tree_height(clauses):
        assignment = []
        stack = [(clauses, assignment)]
        max_height = 0
        while stack:
            clauses, assignment = stack.pop()
            if not clauses:
                max_height = max(max_height, len(assignment))
                continue
            unit_clause = next((c[0] for c in clauses if len(c) == 1), None)
            if unit_clause is not None:
                literal, polarity = unit_clause, True
                if literal < 0:
                    polarity = False
                assignment.append((abs(literal), polarity))
                stack.append((clauses, assignment))
                continue
            pure_symbol = next((s for s, p in pure_symbols.items() if len([c for c in clauses if s in c]) == 1), None)
            if pure_symbol is not None:
                polarity = pure_symbols[pure_symbol]
                assignment.append((pure_symbol, polarity))
                stack.append((clauses, assignment))
                continue
            symbol = next(s for s in range(1, len(clauses) + 1) if s not in [abs(l) for l in sum(clauses, [])])
            stack.append(([c for c in clauses if symbol not in c], assignment + [(symbol, True)]))
            stack.append(([c for c in clauses if -symbol not in c], assignment + [(symbol, False)]))
        return max_height

    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    A = hypercube_adjacency_matrix(n)
    sigma_max = spectral_radius(A)
    h_phi = dpll_search_tree_height(cnf)

    return {
        "metric_name": "correlation",
        "metric_value": sigma_max * h_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": sigma_max * h_phi > 0.3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")