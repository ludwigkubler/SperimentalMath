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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(i, n + 1):
            M[i][j] /= factor
        for k in range(n):
            if k != i:
                factor = M[k][i]
                for j in range(i, n + 1):
                    M[k][j] -= factor * M[i][j]
    return [row[-1] for row in M]

def frobenius_schur_decomposition(A):
    n = len(A)
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    A2 = matrix_multiply(A, A)
    det_A2 = abs(gaussian_elimination(A2, [sum(row) for row in A2])[-1])
    det_I2 = abs(gaussian_elimination(I, [sum(row) for row in I])[-1])
    return det_A2 / det_I2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    instances_tested = 30
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        # Generate a random 3-CNF formula with n variables
        clauses = []
        for _ in range(2 * n):
            literals = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            random.shuffle(literals)
            clause = literals[:3]
            clauses.append(clause)

        # Construct the communication matrix
        M = [[0] * n for _ in range(n)]
        for literal in range(2 * n):
            var = abs(literal) - 1
            sign = -1 if literal < 0 else 1
            for clause in clauses:
                if var + 1 in clause:
                    M[var][clauses.index(clause)] += sign

        # Compute the symmetric square multiplicity using Frobenius-Schur decomposition
        permanent_multiplicity = frobenius_schur_decomposition(M)
        determinant_multiplicity = frobenius_schur_decomposition(matrix_multiply(M, M))

        # Compare the multiplicities
        if permanent_multiplicity <= determinant_multiplicity:
            conjecture_holds = False
            counterexample = "permanent_multiplicity<=determinant_multiplicity"
            break

        metric_value += permanent_multiplicity - determinant_multiplicity

    return {
        "metric_name": "Multiplicity Gap",
        "metric_value": metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")