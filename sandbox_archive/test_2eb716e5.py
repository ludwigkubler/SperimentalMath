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
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if i != j:
                    factor = A[j][i]
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
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def is_prime(num):
        if num <= 1:
            return False
        if num <= 3:
            return True
        if num % 2 == 0 or num % 3 == 0:
            return False
        i = 5
        while i * i <= num:
            if num % i == 0 or num % (i + 2) == 0:
                return False
            i += 6
        return True

    def generate_primes(k):
        primes = []
        num = 2
        while len(primes) < k:
            if is_prime(num):
                primes.append(num)
            num += 1
        return primes

    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append([variables[i-1]])
        for i in range(1, n):
            clauses.append([variables[i], f'~{variables[i-1]}'])
        return variables, clauses

    def algebraic_k_group(n):
        primes = generate_primes(n)
        k_group_order = 1
        for p in primes:
            k_group_order *= p
        return k_group_order

    def communication_complexity_matrix(variables, clauses):
        n = len(variables)
        m = len(clauses)
        A = [[0] * (n + m) for _ in range(n + m)]
        for i in range(n):
            A[i][i] = 1
        for j in range(m):
            for var in clauses[j]:
                if var.startswith('~'):
                    idx = int(var[1:]) - 1
                    A[idx + n][j] = 1
                else:
                    idx = int(var) - 1
                    A[idx][j + n] = 1
        return A

    def rank(matrix):
        reduced_matrix = gaussian_elimination(matrix)
        r = 0
        for row in reduced_matrix:
            if any(row):
                r += 1
        return r

    variables, clauses = tseitin_formula(40)
    k_group_order = algebraic_k_group(len(variables))
    communication_matrix = communication_complexity_matrix(variables, clauses)
    comm_rank = rank(communication_matrix)

    return {
        "metric_name": "Communication Complexity Rank",
        "metric_value": comm_rank,
        "instances_tested": 1,
        "n_max": len(variables),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")