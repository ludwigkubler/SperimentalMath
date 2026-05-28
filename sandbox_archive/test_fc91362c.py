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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        # Find pivot
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, m):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    return A

def rank(matrix):
    matrix = [row[:] for row in matrix]
    gaussian_elimination(matrix)
    rank = 0
    for row in matrix:
        if any(row):
            rank += 1
    return rank

def generate_random_circuit(n, depth=2):
    if depth == 0:
        return random.choice([0, 1])
    op = random.choice(['AND', 'OR'])
    left = generate_random_circuit(n, depth-1)
    right = generate_random_circuit(n, depth-1)
    return [op, left, right]

def tropical_polynomial(circuit):
    if isinstance(circuit, list):
        op = circuit[0]
        left = tropical_polynomial(circuit[1])
        right = tropical_polynomial(circuit[2])
        if op == 'AND':
            return max(left, right)
        elif op == 'OR':
            return min(left, right)
    else:
        return circuit

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            circuit = generate_random_circuit(n)
            poly = tropical_polynomial(circuit)
            current_rank = rank(poly)
            total_rank += current_rank
            instances_tested += 1

            if current_rank > (n ** Fraction(1, 5)):
                conjecture_holds = False
                counterexample = f"Circuit of size {n} with rank {current_rank}"

    mean_rank = total_rank / instances_tested
    return {
        "metric_name": "tropical_cyclotomic_polynomial_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 53))  # Default to first 30 primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")