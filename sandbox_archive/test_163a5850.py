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
    
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def matrix_multiply(A, B):
        m = len(A)
        n = len(B[0])
        p = len(B)
        result = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0 for _ in range(n)]
        for i in range(n - 1, -1, -1):
            x[i] = b[i]
            for j in range(i + 1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        return x
    
    def permutation_circuit_size(perm):
        n = len(perm)
        circuit = [0] * n
        for i in range(n):
            if perm[i] != i:
                j = i
                while perm[j] != j:
                    circuit[perm[j]] += 1
                    j = perm[j]
                circuit[perm[j]] += 1
        return max(circuit)
    
    def affine_root_system_rank(perm):
        n = len(perm)
        A = [[0 for _ in range(n)] for _ in range(n)]
        b = [0 for _ in range(n)]
        for i in range(n):
            A[i][i] = 1
            b[i] = perm[i]
        x = gaussian_elimination(A, b)
        rank = sum(1 for val in x if abs(val) > 1e-9)
        return rank
    
    def generate_random_permutation(n):
        elements = list(range(n))
        random.shuffle(elements)
        return elements
    
    n_min = 5
    n_max = 40
    instances_per_seed = 30
    total_instances = (n_max - n_min + 1) * instances_per_seed
    
    metric_values = []
    conjecture_holds_count = 0
    
    for n in range(n_min, n_max + 1):
        for _ in range(instances_per_seed):
            perm = generate_random_permutation(n)
            rank = affine_root_system_rank(perm)
            circuit_size = permutation_circuit_size(perm)
            metric_values.append(rank / n)
    
    mean_metric_value = sum(metric_values) / total_instances
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / total_instances)
    support_fraction = sum(1 for val in metric_values if val <= 2 * n_min) / len(metric_values)
    
    conjecture_holds = support_fraction >= 0.8
    
    return {
        "metric_name": "Ratio of Minimal Rank to Permutation Length",
        "metric_value": mean_metric_value,
        "instances_tested": total_instances,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio exceeded 2 * n_min for some permutations"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Ratio exceeded 2 * n_min' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")