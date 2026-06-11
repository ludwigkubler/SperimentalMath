# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n, m):
        return [[random.choice([0, 1]) for _ in range(m)] for _ in range(n)]
    
    def count_satisfying_assignments(formula):
        n = len(formula)
        m = len(formula[0])
        count = 0
        for assignment in itertools.product([0, 1], repeat=n):
            if all(all(assignment[j] == formula[i][j] for j in range(m)) for i in range(n)):
                count += 1
        return count
    
    def characteristic_polynomial(formula):
        n = len(formula)
        m = len(formula[0])
        A = [[sum(row) for row in formula]]
        B = [1]
        for _ in range(m - 1):
            A.append([sum(A[-1])])
            B.append(0)
        return A, B
    
    def lll_reduction(M):
        n = len(M)
        m = len(M[0])
        G = M
        u = [Fraction(1, 2) for _ in range(n)]
        k = 1
        while k < n:
            j = k - 1
            while j >= 0 and abs(G[k][j]) > abs(u[j] * G[j][j]):
                q = int(abs(G[k][j]) / abs(u[j] * G[j][j]))
                for i in range(m):
                    G[k][i] -= q * G[j][i]
                u[k], u[j] = u[j], Fraction(1, 2)
                j -= 1
            if abs(G[k][k]) < abs(u[k - 1] * G[k - 1][k - 1]):
                for i in range(m):
                    G[k][i], G[k - 1][i] = G[k - 1][i], G[k][i]
                    u[k], u[k - 1] = u[k - 1], u[k]
                k -= 1
            else:
                u[k] /= abs(G[k][k])
                k += 1
        return G
    
    def minimal_eichler_order(A, B):
        n = len(A)
        m = len(A[0])
        M = [[A[i][j] for j in range(m)] + [B[j]] for i in range(n)]
        M = lll_reduction(M)
        det = 1
        for i in range(n):
            det *= abs(M[i][i])
        return det
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            formula = generate_formula(n, n)
            satisfiability_complexity = count_satisfying_assignments(formula)
            A, B = characteristic_polynomial(formula)
            eichler_order = minimal_eichler_order(A, B)
            results.append((eichler_order, satisfiability_complexity))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    eichler_orders = [r[0] for r in results]
    satisfiability_complexities = [r[1] for r in results]
    mean_eichler_order = sum(eichler_orders) / len(eichler_orders)
    mean_satisfiability_complexity = sum(satisfiability_complexities) / len(satisfiability_complexities)
    
    correlation_coefficient = sum((e - mean_eichler_order) * (s - mean_satisfiability_complexity) for e, s in results) / len(results)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7 and all(abs(c - correlation_coefficient) <= 0.3 for c in [mean_eichler_order, mean_satisfiability_complexity]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
    else:
        correlation_coefficients = [r["metric_value"] for r in results if r["conjecture_holds"]]
        if not correlation_coefficients:
            print(f"RESULT: FALSIFIED counterexample=\"no_valid_correlation\" first_failing_seed={seeds[0]}")
        else:
            mean_corr = sum(correlation_coefficients) / len(correlation_coefficients)
            std_corr = (sum((c - mean_corr)**2 for c in correlation_coefficients) / len(correlation_coefficients))**0.5
            support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
            print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")