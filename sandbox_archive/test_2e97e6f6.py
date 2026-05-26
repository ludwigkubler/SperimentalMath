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

    def is_identity_matrix(M):
        n = len(M)
        for i in range(n):
            for j in range(n):
                if (i == j and M[i][j] != 1) or (i != j and M[i][j] != 0):
                    return False
        return True

    def find_minimal_orbit_length(A):
        m, n = len(A), len(A[0])
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(m)]
        orbit_length = 0
        current_matrix = A
        while not is_identity_matrix(current_matrix):
            current_matrix = matrix_multiplication(current_matrix, A)
            orbit_length += 1
        return orbit_length

    def tseitin_circuit_valuation(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append([variables[i-1]])
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append([-variables[i-1], variables[j-1]])
                clauses.append([-variables[j-1], variables[i-1]])
        return variables, clauses

    def generate_coxeter_group_structure(variables, clauses):
        generators = []
        relations = []
        for var in variables:
            generators.append(var)
        for clause in clauses:
            if len(clause) == 2:
                a, b = clause
                generators.append(f'{a}^{-1}{b}')
                relations.append((f'{a}^{-1}{b}', f'{b}^{-1}{a}'))
        return generators, relations

    def resolution_refutation_size(variables, clauses):
        n = len(variables)
        r = 0
        for clause in clauses:
            if len(clause) == 2:
                r += 1
        return r

    n = random.randint(5, 40)
    variables, clauses = tseitin_circuit_valuation(n)
    generators, relations = generate_coxeter_group_structure(variables, clauses)
    A = [[0] * len(generators) for _ in range(len(generators))]
    for i, gen1 in enumerate(generators):
        for j, gen2 in enumerate(generators):
            if gen1 == gen2:
                A[i][j] = 1
            elif any(gen1.startswith(f'{var}^{-1}') and gen2.startswith(var) for var in variables):
                A[i][j] = -1
    minimal_orbit_length = find_minimal_orbit_length(A)
    resolution_refutation_size_ = resolution_refutation_size(variables, clauses)
    
    if minimal_orbit_length < 2 ** math.ceil(math.log(resolution_refutation_size_, 2)):
        conjecture_holds = False
        counterexample = f"n={n}, r(n)={resolution_refutation_size_}, ω(G)={minimal_orbit_length}"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "minimal_orbit_length",
        "metric_value": minimal_orbit_length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")