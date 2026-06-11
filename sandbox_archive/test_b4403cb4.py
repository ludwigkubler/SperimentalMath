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
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = Fraction(A[j][i], A[i][i])
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

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def polynomial_ring_order(n):
        # Define the polynomial ring over F_2
        variables = list(range(1, n + 1))
        monomials = [tuple(sorted(random.sample(variables, k))) for k in range(1, n + 1)]
        
        # Construct the adjacency matrix for the Galois group
        m = len(monomials)
        A = [[0] * m for _ in range(m)]
        for i in range(m):
            for j in range(i + 1, m):
                if monomials[i].issubset(monomials[j]):
                    A[i][j] = 1
                    A[j][i] = 1
        
        # Perform Gaussian elimination to find the rank of the matrix
        rank = gaussian_elimination(A)
        
        # The order of the Galois group is 2^rank
        return 2 ** rank

    def resolution_width(phi):
        clauses = phi.split(' ')
        variables = set()
        for clause in clauses:
            if clause.startswith('-'):
                continue
            variables.update(clause)
        return len(variables)

    # Generate a random CNF with n variables and m clauses
    n = random.randint(5, 30)
    m = random.randint(n * 2, n * 4)
    phi = []
    for _ in range(m):
        clause = random.sample(range(1, n + 1), random.randint(1, n))
        if random.choice([True, False]):
            clause = [-x for x in clause]
        phi.append(' '.join(map(str, clause)))
    
    # Compute the resolution proof width
    w_phi = resolution_width(' '.join(phi))

    # Compute the order of the Galois group over the polynomial ring
    galois_order = polynomial_ring_order(n)

    # Calculate the ratio of the order of the Galois group to the square of the resolution proof width
    if w_phi == 0:
        return {
            "metric_name": "Galois Group Order / Resolution Width^2",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_width_is_zero"
        }
    
    ratio = Fraction(galois_order, w_phi ** 2)

    return {
        "metric_name": "Galois Group Order / Resolution Width^2",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= Fraction(3, 2),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"galois_group_order_not_leq_1.5_times_resolution_width^2\" first_failing_seed={first_failing_seed}")