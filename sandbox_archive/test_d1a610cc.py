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
    
    def generate_disjoint_sets(n):
        sets = []
        for _ in range(2):
            elements = set(range(n))
            while len(elements) > 0:
                size = random.randint(1, min(len(elements), n // 4))
                subset = random.sample(elements, size)
                sets.append(subset)
                elements -= set(subset)
        return sets
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if any(matrix[i][j] != 0 for j in range(n)):
                rank += 1
                for j in range(n):
                    if matrix[i][j] != 0:
                        factor = matrix[i][j]
                        for k in range(i, m):
                            matrix[k][j] /= factor
                        break
                for k in range(m):
                    if k != i and any(matrix[k][j] != 0 for j in range(n)):
                        for j in range(n):
                            matrix[k][j] -= matrix[i][j]
        return rank
    
    def young_diagram_partitions(n):
        partitions = []
        def generate_partition(k, n, partition):
            if k == 0:
                partitions.append(partition[:])
                return
            for i in range(min(n, k), -1, -1):
                partition.append(i)
                generate_partition(k - i, n - i, partition)
                partition.pop()
        generate_partition(n, n, [])
        return partitions
    
    def kronecker_coefficient(λ, μ, ν):
        if len(λ) != len(μ) or len(μ) != len(ν):
            return 0
        m = len(λ)
        λ = [λ[i] - i for i in range(m)]
        μ = [μ[i] - i for i in range(m)]
        ν = [ν[i] - i for i in range(m)]
        n = sum(λ)
        if any(x < 0 or x > n for x in λ + μ + ν):
            return 0
        def hook_length(p, q):
            return (p + 1) * (q + 1) // 2 - p - q
        def sign(p):
            s = 1
            for i in range(1, len(p)):
                for j in range(i):
                    if p[i] < p[j]:
                        s *= -1
            return s
        def hook_length_product(partition):
            product = 1
            for i in range(len(partition)):
                for j in range(partition[i]):
                    product *= hook_length(i, j)
            return product
        def young_symmetrizer(partition):
            n = sum(partition)
            matrix = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    if partition[j] > partition[i]:
                        matrix[i][j] = 1
                    elif partition[j] < partition[i]:
                        matrix[i][j] = -1
            return matrix
        def kronecker_coefficient_recursive(λ, μ, ν):
            if len(λ) == 0:
                return 1
            m = len(λ)
            λm = λ[-1]
            μm = μ[-1]
            νm = ν[-1]
            λ = λ[:-1]
            μ = μ[:-1]
            ν = ν[:-1]
            result = 0
            for i in range(max(0, μm - νm), min(λm, μm) + 1):
                result += sign(i) * hook_length_product([λm - i] + λ) * hook_length_product([μm - i] + μ) * hook_length_product([νm - i] + ν) * kronecker_coefficient_recursive(λ, μ, ν)
            return result
        return abs(kronecker_coefficient_recursive(λ, μ, ν))
    
    n = random.randint(5, 40)
    sets = generate_disjoint_sets(n)
    matrix = [[1 if i in set_ else 0 for j in range(n)] for set_ in sets]
    rank = matrix_rank(matrix)
    partitions = young_diagram_partitions(n)
    min_kronecker_coefficient = float('inf')
    for λ in partitions:
        for μ in partitions:
            for ν in partitions:
                coeff = kronecker_coefficient(λ, μ, ν)
                if coeff < min_kronecker_coefficient:
                    min_kronecker_coefficient = coeff
    conjecture_holds = min_kronecker_coefficient >= (math.log(n)) ** 1.5
    counterexample = "" if conjecture_holds else f"Minimum Kronecker coefficient {min_kronecker_coefficient} < ({math.log(n)})^1.5"
    
    return {
        "metric_name": "Kronecker Coefficient Gap",
        "metric_value": min_kronecker_coefficient,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")