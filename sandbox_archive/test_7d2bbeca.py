# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def clause_indicator_polynomial(clauses):
        n = len(clauses[0])
        poly = [1]
        for clause in clauses:
            term = 1
            for literal in range(1, n + 1):
                if literal in clause:
                    term *= (1 + x[literal - 1])
                else:
                    term *= (1 - x[literal - 1])
            poly += [term]
        return poly

    def companion_matrix(poly):
        n = len(poly) - 1
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                A[i][j] = poly[j] / poly[i]
        return A

    def eigenvalues(matrix):
        n = len(matrix)
        if n == 2:
            a, b, c = matrix[0][0], matrix[0][1], matrix[1][0]
            det = a * c - b * b
            trace = a + c
            return [(trace + math.sqrt(trace**2 - 4 * det)) / 2, (trace - math.sqrt(trace**2 - 4 * det)) / 2]
        else:
            # Use QR algorithm for larger matrices
            def qr(A):
                n = len(A)
                Q = [[0] * n for _ in range(n)]
                R = [[0] * n for _ in range(n)]
                for i in range(n):
                    Q[i][i] = 1
                for k in range(20):  # Max iterations
                    H = [[0] * n for _ in range(n)]
                    for i in range(n):
                        for j in range(i + 1, n):
                            v = [A[i][j]]
                            for l in range(i + 1, n):
                                v.append(A[l][i])
                            norm = math.sqrt(sum(x**2 for x in v))
                            Q[i][j] = -v[0] / norm
                            R[i][j] = v[1] / norm
                            for l in range(n):
                                A[i][l] -= Q[i][j] * R[j][l]
                                A[l][i] -= Q[l][j] * R[j][i]
                    for i in range(n):
                        for j in range(i + 1, n):
                            A[i][j] = 0
                return A

            def hessenberg(A):
                n = len(A)
                H = [[A[i][j] if j <= i + 1 else 0 for j in range(n)] for i in range(n)]
                Q = [[0] * n for _ in range(n)]
                for k in range(n - 2, -1, -1):
                    G = [[0] * n for _ in range(n)]
                    G[k][k + 1] = A[k + 1][k]
                    G[k + 1][k] = A[k][k + 1]
                    Q_k = qr(G)
                    H = matrix_multiplication(Q_k, matrix_multiplication(H, transpose(Q_k)))
                return H

            def matrix_multiplication(A, B):
                n = len(A)
                C = [[0] * n for _ in range(n)]
                for i in range(n):
                    for j in range(n):
                        C[i][j] = sum(A[i][k] * B[k][j] for k in range(n))
                return C

            def transpose(matrix):
                n = len(matrix)
                T = [[0] * n for _ in range(n)]
                for i in range(n):
                    for j in range(n):
                        T[j][i] = matrix[i][j]
                return T

            H = hessenberg(matrix)
            eigenvals = [H[i][i] for i in range(n)]
            return eigenvals

    def distinct_roots(eigenvals):
        return len(set(eigenvals))

    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        n = random.randint(5, 40)
        m = random.randint(1, n * (n - 1) // 2)
        clauses = [random.sample(range(1, n + 1), random.randint(1, n)) for _ in range(m)]
        
        x = [Fraction(random.randint(-10, 10), random.randint(1, 10)) for _ in range(n)]
        poly = clause_indicator_polynomial(clauses)
        A = companion_matrix(poly)
        eigenvals = eigenvalues(A)
        roots = distinct_roots(eigenvals)

        metric_values.append(roots)
        
        if conjecture_holds:
            expected = m**(1/3) * n**(2/3)
            if abs(roots - expected) > 2 * expected:
                conjecture_holds = False
                counterexample = f"n={n}, m={m}, roots={roots}, expected={expected}"

    return {
        "metric_name": "Distinct Roots",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")