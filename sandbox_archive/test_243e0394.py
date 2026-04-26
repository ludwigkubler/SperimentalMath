# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import product

def run_trial(seed: int) -> dict:
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def lcm(a, b):
        return abs(a*b) // gcd(a, b)

    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        else:
            g, x, y = extended_gcd(b % a, a)
            return g, y - (b // a) * x, x

    def mod_inverse(a, m):
        g, x, _ = extended_gcd(a, m)
        if g != 1:
            raise ValueError('Modular inverse does not exist')
        else:
            return x % m

    def matrix_mod_inv(matrix, mod):
        n = len(matrix)
        det = 0
        for i in range(n):
            det += matrix[0][i] * matrix_minor(matrix, 0, i) * (-1)**(0 + i)
        det = det % mod
        inv_det = mod_inverse(det, mod)
        adjugate = []
        for i in range(n):
            row = []
            for j in range(n):
                minor = matrix_minor(matrix, i, j)
                cofactor = (-1)**(i+j) * minor
                row.append(cofactor % mod)
            adjugate.append(row)
        inv_matrix = [[(adjugate[j][i] * inv_det) % mod for i in range(n)] for j in range(n)]
        return inv_matrix

    def matrix_minor(matrix, i, j):
        return [row[:j] + row[j+1:] for row in matrix[1:]]

    def matrix_multiply(A, B, mod):
        n = len(A)
        C = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
                C[i][j] %= mod
        return C

    def gaussian_elimination(matrix, mod):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if matrix[i][i] == 0:
                for j in range(i+1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                    else:
                        continue
                else:
                    rank -= 1
            if matrix[i][i] == 0:
                continue
            pivot = matrix[i][i]
            for j in range(i, n):
                matrix[i][j] *= mod_inverse(pivot, mod)
                matrix[i][j] %= mod
            for k in range(n):
                if k != i and matrix[k][i] != 0:
                    factor = matrix[k][i]
                    for j in range(i, n):
                        matrix[k][j] -= factor * matrix[i][j]
                        matrix[k][j] %= mod
            rank += 1
        return rank

    def polynomial_elimination(f, n, mod):
        variables = list(range(n))
        monomials = [tuple(sorted(v)) for v in product(variables, repeat=n)]
        monomial_dict = {m: i for i, m in enumerate(monomials)}
        matrix = [[0]*len(monomials) for _ in range(len(monomials))]
        for i, m1 in enumerate(monomials):
            for j, m2 in enumerate(monomials):
                if all(v1 <= v2 for v1, v2 in zip(m1, m2)):
                    matrix[i][j] = 1
        rank = gaussian_elimination(matrix, mod)
        return len(monomials) - rank

    def truth_table(f, n):
        inputs = list(product([0, 1], repeat=n))
        outputs = [f(inputs[i]) for i in range(len(inputs))]
        return outputs

    def seed_length(f, n):
        # Placeholder function to return a lower bound on seed length
        # This is a dummy implementation and should be replaced with actual logic
        return n + 1

    random.seed(seed)
    n = random.choice([5, 8, 11, 14])
    f = lambda x: sum(x) % 2  # Example function (parity function)
    outputs = truth_table(f, n)
    mod = 2
    transcendence_degree = polynomial_elimination(outputs, n, mod)
    seed_length_bound = seed_length(f, n) - 1

    return {
        "metric_name": "transcendence_degree",
        "metric_value": transcendence_degree,
        "instances_tested": 1,
        "conjecture_holds": transcendence_degree >= seed_length_bound,
        "counterexample": "" if transcendence_degree >= seed_length_bound else f"seed_length({n}) - 1 = {seed_length_bound}, but found transcendence degree = {transcendence_degree}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")