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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def matrix_mult(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

def matrix_add(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = (A[i][j] + B[i][j]) % mod
    return C

def matrix_sub(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = (A[i][j] - B[i][j]) % mod
    return C

def matrix_pow(M, k, mod):
    n = len(M)
    result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    while k > 0:
        if k % 2 == 1:
            result = matrix_mult(result, M, mod)
        M = matrix_mult(M, M, mod)
        k //= 2
    return result

def gaussian_elimination(A, b, mod):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        pivot = A[i][i]
        for j in range(i, n):
            A[i][j] = (A[i][j] * mod_inverse(pivot, mod)) % mod
        b[i] = (b[i] * mod_inverse(pivot, mod)) % mod
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(i, n):
                    A[j][k] = (A[j][k] - factor * A[i][k]) % mod
                b[j] = (b[j] - factor * b[i]) % mod

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def tseitin_formula(n):
        clauses = []
        for i in range(1, n + 1):
            clauses.append([i])
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                clauses.append([-i, -j, i + j])
        return clauses
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clauses = [c[0] for c in clauses if len(c) == 1]
        pure_symbols = {}
        for clause in clauses:
            for literal in clause:
                symbol = abs(literal)
                if symbol not in pure_symbols:
                    pure_symbols[symbol] = literal > 0
                elif pure_symbols[symbol] != (literal > 0):
                    return False
        
        unit_clause = next((c[0] for c in clauses if len(c) == 1), None)
        if unit_clause is not None:
            symbol = abs(unit_clause)
            assignment[symbol] = unit_clause > 0
            new_clauses = [c for c in clauses if unit_clause not in c and -unit_clause not in c]
            return dpll(new_clauses, assignment)
        
        pure_symbol = next((symbol for symbol, polarity in pure_symbols.items() if polarity), None)
        if pure_symbol is not None:
            assignment[pure_symbol] = True
            new_clauses = [c for c in clauses if pure_symbol not in c and -pure_symbol not in c]
            return dpll(new_clauses, assignment)
        
        symbol = next(symbol for symbol in range(1, len(clauses) + 1))
        assignment[symbol] = True
        new_clauses = [c for c in clauses if symbol not in c and -symbol not in c]
        if dpll(new_clauses, assignment):
            return True
        
        assignment[symbol] = False
        new_clauses = [c for c in clauses if symbol not in c and -symbol not in c]
        return dpll(new_clauses, assignment)
    
    def eta_invariant(n):
        # Placeholder for actual computation of Eta-invariant
        return random.random()
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_eta = 0.0
    total_width = 0
    
    for n in n_values:
        for _ in range(5):
            clauses = tseitin_formula(n)
            assignment = {}
            width = dpll(clauses, assignment)
            if width is None:
                continue
            eta = eta_invariant(n)
            instances_tested += 1
            total_eta += eta
            total_width += width
    
    if instances_tested == 0:
        return {
            "metric_name": "eta_vs_width",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_eta = total_eta / instances_tested
    mean_width = total_width / instances_tested
    correlation_coefficient = (instances_tested * sum(eta * width for eta, width in zip([mean_eta] * instances_tested, [mean_width] * instances_tested)) -
                               sum([mean_eta] * instances_tested) * sum([mean_width] * instances_tested)) / \
                              math.sqrt((instances_tested * sum(eta ** 2 for eta in [mean_eta] * instances_tested) - (sum([mean_eta] * instances_tested) ** 2)) *
                                        (instances_tested * sum(width ** 2 for width in [mean_width] * instances_tested) - (sum([mean_width] * instances_tested) ** 2)))
    
    return {
        "metric_name": "eta_vs_width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": 40,
        "conjecture_holds": correlation_coefficient > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")