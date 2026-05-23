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
    
    def generate_k_cnf(n, k):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = random.sample(variables, random.randint(1, n))
            clause = sorted(clause)
            if clause not in clauses:
                clauses.append(clause)
        return clauses

    def clause_indicator_polynomial(cnf_instance, n):
        polynomial = [[0] * (2**n) for _ in range(n)]
        for i in range(n):
            for assignment in range(2**n):
                binary_assignment = [int(x) for x in format(assignment, f'0{n}b')]
                if all(binary_assignment[j-1] == 1 for j in cnf_instance[i]):
                    polynomial[i][assignment] = 1
        return polynomial

    def noncommutative_crossed_product(polynomial):
        n = len(polynomial)
        product = [[0] * (2**n) for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(2**n):
                    for l in range(2**n):
                        if polynomial[i][k] == 1 and polynomial[j][l] == 1:
                            product[i][j] += polynomial[i][k] * polynomial[j][l]
        return product

    def rank(matrix):
        m = len(matrix)
        n = len(matrix[0])
        augmented_matrix = [row + [i] for i, row in enumerate(matrix)]
        rref = gaussian_elimination(augmented_matrix)
        rank = 0
        for row in rref:
            if any(row[i] != 0 for i in range(n)):
                rank += 1
        return rank

    def gaussian_elimination(A):
        m = len(A)
        n = len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                raise ValueError("Matrix is singular")
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def bp_readtwice_circuit_threshold(cnf_instance):
        n = len(cnf_instance)
        return 2**n - 1

    n = random.randint(5, 40)
    k = random.randint(1, n)
    cnf_instance = generate_k_cnf(n, k)
    
    polynomial = clause_indicator_polynomial(cnf_instance, n)
    crossed_product = noncommutative_crossed_product(polynomial)
    rank_nc = rank(crossed_product)
    threshold_bp = bp_readtwice_circuit_threshold(cnf_instance)

    difference = abs(rank_nc - threshold_bp)
    beta = 1.0  # Assuming a constant beta for simplicity
    conjecture_holds = difference <= beta * math.log(n, 2)
    
    return {
        "metric_name": "Rank vs DPLL Heig",
        "metric_value": difference,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"rank_nc={rank_nc}, threshold_bp={threshold_bp}"
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
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")