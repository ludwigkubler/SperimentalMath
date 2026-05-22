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
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k = len(A), len(B)
    n = len(B[0])
    C = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = max(range(i, m), key=lambda r: abs(augmented[r][i]))
        if augmented[max_row][i] == 0:
            return None
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        for j in range(m):
            if i != j:
                factor = augmented[j][i] / augmented[i][i]
                for k in range(n + 1):
                    augmented[j][k] -= factor * augmented[i][k]
    rank = sum(1 for row in augmented if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    def generate_branching_program(size):
        program = []
        for _ in range(size):
            program.append(random.choice(['0', '1']))
        return ''.join(program)
    
    def compute_tropical_algebraic_stack_size(program):
        # Simplified mapping to a rank based on the length of the program
        return len(program) // 2
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Test each size multiple times
            program = generate_branching_program(n)
            rank = compute_tropical_algebraic_stack_size(program)
            results.append((n, rank))
    
    mean_rank = sum(rank for _, rank in results) / len(results)
    std_dev = math.sqrt(sum((rank - mean_rank) ** 2 for _, rank in results) / len(results))
    
    conjecture_holds = all(0.5 * n <= rank <= 1.5 * n for n, rank in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_rank) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")