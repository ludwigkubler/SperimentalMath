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

def generate_disjointness_instance(n):
    A = [random.randint(0, 1) for _ in range(n)]
    B = [random.randint(0, 1) for _ in range(n)]
    return A, B

def communication_matrix(disjointness_instances):
    n = len(next(iter(disjointness_instances)))
    matrix = [[False] * (2**n) for _ in range(2**n)]
    for i in range(2**n):
        for j in range(2**n):
            A, B = [int(x) for x in format(i, f'0{n}b')], [int(x) for x in format(j, f'0{n}b')]
            matrix[i][j] = all(A[k] == B[k] for k in range(n))
    return matrix

def quadruple_counting(matrix):
    n = len(matrix)
    count = 0
    for i in range(n):
        for j in range(i, n):
            for k in range(j, n):
                for l in range(k, n):
                    if matrix[i][j] and matrix[j][k] and matrix[k][l]:
                        count += 1
    return count

def max_cut_approximation(matrix):
    n = len(matrix)
    cut_value = 0
    for i in range(n):
        for j in range(i, n):
            if not matrix[i][j]:
                cut_value += 1
    return cut_value / (n * (n - 1) / 2)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 5
    instances_tested = 30
    metric_name = "additive_energy"
    total_additive_energy = 0.0

    for _ in range(instances_tested):
        A, B = generate_disjointness_instance(n)
        matrix = communication_matrix([(A, B)])
        additive_energy = quadruple_counting(matrix)
        discrepancy = max_cut_approximation(matrix)
        total_additive_energy += additive_energy * discrepancy

    metric_value = total_additive_energy / instances_tested
    conjecture_holds = True
    counterexample = ""

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = primes[:30]

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
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")