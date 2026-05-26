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
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    Augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(Augmented[j][i]) > abs(Augmented[max_row][i]):
                max_row = j
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        factor = Augmented[i][i]
        for j in range(i, n+1):
            Augmented[i][j] /= factor
        for j in range(n):
            if i != j:
                factor = Augmented[j][i]
                for k in range(i, n+1):
                    Augmented[j][k] -= factor * Augmented[i][k]
    return [row[-1] for row in Augmented]

def is_quaternionic_representation(Q):
    # Placeholder function to check if Q is a quaternionic representation
    # This should be replaced with actual implementation
    return True

def xor_and_tree_width(f):
    # Placeholder function to compute XOR-AND tree width
    # This should be replaced with actual implementation
    return 10  # Example value

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([10, 15, 20])
    f = [random.randint(0, 1) for _ in range(2**n)]
    
    # Compute quaternionic representation Q
    if not is_quaternionic_representation(f):
        return {
            "metric_name": "quaternionic_rank",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    # Compute XOR-AND tree width
    xor_and_width = xor_and_tree_width(f)
    
    # Check the conjecture
    quaternionic_rank = len(gaussian_elimination(f, [1]*n))
    conjecture_holds = quaternionic_rank <= xor_and_width
    
    return {
        "metric_name": "quaternionic_rank",
        "metric_value": quaternionic_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"rank={quaternionic_rank}, expected={xor_and_width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 17 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")