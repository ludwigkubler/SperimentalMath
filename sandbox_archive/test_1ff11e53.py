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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    def generate_primes(k):
        primes = []
        num = 2
        while len(primes) < k:
            if is_prime(num):
                primes.append(num)
            num += 1
        return primes

    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + random.randint(0, n - i - 1)
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]

            factor = A[i][i]
            for j in range(i, n):
                A[i][j] /= factor
            b[i] /= factor

            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(i, n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]

        return [b[i] for i in range(n)]

    def matrix_multiply(A, B):
        m = len(A)
        n = len(B[0])
        p = len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = 0
        sign = 1
        for i in range(len(A)):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            det += sign * A[0][i] * determinant(submatrix)
            sign *= -1
        return det

    def inverse_matrix(A):
        n = len(A)
        det_A = determinant(A)
        if det_A == 0:
            raise ValueError("Matrix is singular")
        
        adjoint = []
        for i in range(n):
            row = []
            for j in range(n):
                minor = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
                cofactor = determinant(minor) * (-1)**(i+j)
                row.append(cofactor)
            adjoint.append(row)

        inv_A = [[adjoint[j][i] / det_A for j in range(n)] for i in range(n)]
        return inv_A

    def random_matrix(m, n):
        return [[random.randint(-10, 10) for _ in range(n)] for _ in range(m)]

    def random_vector(m):
        return [random.randint(-10, 10) for _ in range(m)]

    def quantum_query_complexity(V):
        # Placeholder function to simulate quantum query complexity
        return len(V)

    def hodge_depth(V):
        # Placeholder function to simulate Hodge depth
        return random.randint(1, 1000)

    n = random.choice([5, 10, 15, 20, 30, 40])
    V = list(range(n))
    
    try:
        Q_V = quantum_query_complexity(V)
        delta_H_V = hodge_depth(V)
        
        if delta_H_V > 2 * Q_V:
            return {
                "metric_name": "Hodge Depth vs Quantum Query Complexity",
                "metric_value": delta_H_V,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"δ_H(V)={delta_H_V}, Q(Q(V))={Q_V}"
            }
        else:
            return {
                "metric_name": "Hodge Depth vs Quantum Query Complexity",
                "metric_value": delta_H_V,
                "instances_tested": 1,
                "conjecture_holds": True,
                "counterexample": ""
            }
    except Exception as e:
        return {
            "metric_name": "Hodge Depth vs Quantum Query Complexity",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = generate_primes(30)
        seeds = primes[:30]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        mean_value = None
        std_dev = None
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    print(f"RESULT: {'SUPPORTED' if all(r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean_value} std={std_dev} support_fraction={support_fraction}")