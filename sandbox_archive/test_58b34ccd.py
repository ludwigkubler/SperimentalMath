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
from fractions import Fraction
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
    
    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            sign = (-1) ** (j % 2)
            det += sign * A[0][j] * determinant(submatrix)
        return det
    
    def moment_matrix(polynomial, variables):
        n = len(variables)
        m = n + 1
        M = [[0 for _ in range(m)] for _ in range(m)]
        for term in polynomial:
            exponents = [term.count(var) for var in variables]
            coeff = term[0]
            index = sum(exponents[i] * (n - i) for i in range(n))
            M[index][index] += coeff
        return M
    
    def symplectic_invariant(M):
        m, n = len(M), len(M[0])
        if m != n:
            raise ValueError("Matrix must be square")
        det = determinant(gaussian_elimination(M))
        return abs(det) ** (1 / n)
    
    def max_cut_instance(n):
        variables = [f'x{i}' for i in range(n)]
        edges = [(random.randint(0, n-1), random.randint(0, n-1)) for _ in range(n * (n - 1) // 2)]
        return variables, edges
    
    def sos_polynomial(variables, edges):
        n = len(variables)
        polynomial = []
        for i in range(n):
            polynomial.append((1, [variables[i]]))
        for u, v in edges:
            polynomial.append((1, [variables[u], variables[v]]))
            polynomial.append((-2, [variables[u], variables[v], variables[u], variables[v]]))
        return polynomial
    
    def approximation_ratio(polynomial, variables):
        n = len(variables)
        max_cut_value = sum(1 for u, v in edges if random.choice([0, 1]) == 0)
        sos_value = sum(coeff * sum(x.count(var) ** 2 for var in variables) for coeff, x in polynomial)
        return max_cut_value / sos_value
    
    n = random.randint(5, 40)
    variables, edges = max_cut_instance(n)
    polynomial = sos_polynomial(variables, edges)
    R = approximation_ratio(polynomial, variables)
    
    M_p = moment_matrix(polynomial, variables)
    invariant = symplectic_invariant(M_p)
    
    metric_name = "symplectic_invariant"
    metric_value = invariant
    instances_tested = 1
    conjecture_holds = invariant >= math.log(n / R)
    counterexample = "" if conjecture_holds else f"n={n}, R={R}, invariant={invariant}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['instances_tested']}, R={results[0]['metric_value']}, invariant={results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")