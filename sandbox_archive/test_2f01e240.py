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
    def permute(lst):
        return [lst[i] for i in random.sample(range(len(lst)), len(lst))]

    def sign_permute(lst):
        return [-1 if i % 2 else 1 for i in range(len(lst))]

    def identity_matrix(n):
        return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        sign = 1
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += sign * matrix[0][j] * determinant(submatrix)
            sign *= -1
        return det

    def permanent(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        perm = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            sign = (-1) ** (n - 1 - j)
            perm += sign * matrix[0][j] * permanent(submatrix)
        return perm

    def frobenius_norm(matrix):
        n = len(matrix)
        norm = 0
        for i in range(n):
            for j in range(n):
                norm += abs(matrix[i][j]) ** 2
        return math.sqrt(norm)

    def projection(matrix, idempotent):
        n = len(matrix)
        proj = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                proj[i][j] = sum(idempotent[k][l] * matrix[k][j] for k in range(n) for l in range(n))
        return proj

    def matching_coefficient(matrix, idempotent):
        n = len(matrix)
        coeff = [0] * math.factorial(n)
        for perm in itertools.permutations(range(n)):
            sign = 1
            val = 1
            for i in range(n):
                val *= matrix[perm[i]][i]
            coeff[id(perm)] += sign * val
        return [coeff[id(perm)] / frobenius_norm(matrix) ** n for perm in itertools.permutations(range(n))]

    def specht_block_count(coeff, idempotent):
        n = len(coeff)
        count = 0
        for λ in partitions(n):
            norm_squared = sum(abs(sum(coeff[g] * idempotent[g][t] for g in range(math.factorial(n))) ** 2) for t in range(math.factorial(n)))
            if norm_squared / frobenius_norm(coeff) ** 2 > 1e-9:
                count += 1
        return count

    def partitions(n):
        def partition(n, k):
            if n == 0:
                yield []
            elif k == 0 or k > n:
                pass
            else:
                for p in partition(n - k, k):
                    yield [k] + p
                yield from partition(n, k - 1)
        return list(partition(n, n))

    def random_invertible_matrix(n):
        matrix = identity_matrix(n)
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    matrix[i][j], matrix[j][i] = -matrix[j][i], -matrix[i][j]
                else:
                    matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        return matrix

    def lift_permutation(perm, L):
        n = len(perm)
        lifted = identity_matrix(n)
        for i in range(n):
            for j in range(n):
                lifted[i][j] = L[perm[i]][j]
        return lifted

    def lift_determinant(det, L):
        n = len(det)
        lifted = identity_matrix(n)
        for i in range(n):
            for j in range(n):
                lifted[i][j] = L[i][det[j]]
        return lifted

    random.seed(seed)

    if seed == 0:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    else:
        seeds = [seed]

    results = []
    for n in [4, 5]:
        if seed == 0 and n not in seeds:
            continue

        perm_coeff = matching_coefficient(identity_matrix(n), identity_matrix(n))
        det_coeff = matching_coefficient(sign_permute(identity_matrix(n)), identity_matrix(n))

        if specht_block_count(perm_coeff, identity_matrix(n)) != 1 or specht_block_count(det_coeff, identity_matrix(n)) != 1:
            return {
                "metric_name": "specht_block_count",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "sanity_check_failed"
            }

        for _ in range(30):
            L = random_invertible_matrix(n)
            perm_lifted_coeff = matching_coefficient(lift_permutation(identity_matrix(n), L), identity_matrix(n))
            det_lifted_coeff = matching_coefficient(lift_determinant(sign_permute(identity_matrix(n)), L), identity_matrix(n))

            perm_count = specht_block_count(perm_lifted_coeff, identity_matrix(n))
            det_count = specht_block_count(det_lifted_coeff, identity_matrix(n))

            if perm_count <= det_count:
                return {
                    "metric_name": "specht_block_count",
                    "metric_value": None,
                    "instances_tested": 0,
                    "conjecture_holds": False,
                    "counterexample": f"seed={seed}, n={n}, L={L}"
                }

            results.append({
                "metric_name": "specht_block_count",
                "metric_value": perm_count - det_count,
                "instances_tested": 1,
                "conjecture_holds": True,
                "counterexample": ""
            })

    mean = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["metric_value"] >= 1) / len(results)

    return {
        "metric_name": "specht_block_count",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["metric_value"] >= 1) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(result["conjecture_holds"] is False for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")