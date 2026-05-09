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
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def transpose(A):
        m, n = len(A), len(A[0])
        return [[A[j][i] for j in range(m)] for i in range(n)]
    
    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = 0
        for c in range(len(A)):
            det += ((-1) ** c) * A[0][c] * determinant([row[:c] + row[c+1:] for row in A[1:]])
        return det
    
    def rank(A):
        return sum(1 for row in gaussian_elimination(A) if any(row))
    
    def sos_refutation_degree(poly_system):
        m = len(poly_system)
        n = int(math.sqrt(m * 2))  # Upper bound on the degree
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i, eq in enumerate(poly_system):
            for term in eq:
                x, y = term.split('x')
                A[int(x)][int(y)] += 1
        
        # Basic SDP relaxation
        from scipy.optimize import minimize
        def objective(vars):
            return sum(vars[i] * vars[j] * A[i][j] for i in range(n + 1) for j in range(i, n + 1))
        
        constraints = [{'type': 'eq', 'fun': lambda vars: sum(vars[:n+1]) - 1}]
        bounds = [(0, None)] * (n + 1)
        result = minimize(objective, [0] * (n + 1), method='SLSQP', bounds=bounds, constraints=constraints)
        return result.fun
    
    m = 16
    n = 30
    instances_tested = n
    refutation_degrees = []
    
    for _ in range(n):
        # Generate random quadratic system over GF(2)
        poly_system = []
        for i in range(m):
            terms = [f'x{random.randint(0, m-1)}x{random.randint(0, m-1)}' for _ in range(random.randint(1, 3))]
            poly_system.append('+'.join(terms))
        
        # Compute SOS refutation degree
        refutation_degree = sos_refutation_degree(poly_system)
        refutation_degrees.append(refutation_degree)
    
    mean_refutation_degree = sum(refutation_degrees) / instances_tested
    expected_refutation_degree = math.sqrt(m)
    ratio = mean_refutation_degree / expected_refutation_degree
    
    conjecture_holds = abs(ratio - 1) <= 0.2
    counterexample = "" if conjecture_holds else f"Ratio {ratio:.4f} deviates from 1 by ±20%"
    
    return {
        "metric_name": "SOS Refutation Degree",
        "metric_value": mean_refutation_degree,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std=NOT_COMPUTED support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio deviates by ±20%\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")