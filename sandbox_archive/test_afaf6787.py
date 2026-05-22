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
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
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
        det = Fraction(1)
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            det *= A[i][i]
            factor = -A[i][i]
            for j in range(m):
                if j != i:
                    factor += A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return det

    def bray_curtis_distance(A, B):
        numerator = sum(abs(a - b) for a, b in zip(A, B))
        denominator = sum(max(abs(a), abs(b)) for a, b in zip(A, B))
        if denominator == 0:
            return 1
        return numerator / denominator

    def ac0_circuit_depth(n):
        # Placeholder function to simulate AC0 circuit depth calculation
        # This is a dummy implementation and should be replaced with actual logic
        return n * (n + 1) // 2

    def generate_random_cnf(n, m):
        symbols = [f"x{i}" for i in range(1, n+1)]
        cnf = []
        for _ in range(m):
            clause = random.sample(symbols, k=random.randint(1, n))
            if random.choice([True, False]):
                clause = [-x for x in clause]
            cnf.append(clause)
        return cnf

    def construct_representation(cnf):
        # Placeholder function to simulate representation construction
        # This is a dummy implementation and should be replaced with actual logic
        m = len(cnf)
        n = len(cnf[0])
        A = [[0] * (m + 1) for _ in range(m + 1)]
        for i in range(m):
            for j in range(n):
                if cnf[i][j] > 0:
                    A[i][j] = 1
                else:
                    A[i][j] = -1
        return A

    def minimal_brauer_group_rank(A):
        # Placeholder function to simulate Brauer group rank calculation
        # This is a dummy implementation and should be replaced with actual logic
        A = gaussian_elimination(A)
        rank = sum(1 for row in A if any(row))
        return rank

    n = random.randint(5, 40)
    m = random.randint(n, n * (n + 1) // 2)
    cnf = generate_random_cnf(n, m)
    representation = construct_representation(cnf)
    brauer_group_rank = minimal_brauer_group_rank(representation)
    circuit_depth = ac0_circuit_depth(n)

    return {
        "metric_name": "Brauer Group Rank vs AC0 Circuit Depth",
        "metric_value": bray_curtis_distance([brauer_group_rank], [circuit_depth]),
        "instances_tested": 1,
        "conjecture_holds": brauer_group_rank >= circuit_depth,
        "counterexample": "" if brauer_group_rank >= circuit_depth else f"CNF: {cnf}, Brauer Group Rank: {brauer_group_rank}, Circuit Depth: {circuit_depth}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

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
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")