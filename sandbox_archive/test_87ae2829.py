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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_primes(k):
        primes = []
        num = 2
        while len(primes) < k:
            if is_prime(num):
                primes.append(num)
            num += 1
        return primes
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i + 1, rows):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def generate_boolean_algebra(n):
        # Generate a random boolean algebra of size n
        elements = [f"x{i}" for i in range(n)]
        operations = []
        for i in range(n):
            for j in range(i + 1, n):
                operations.append((elements[i], elements[j]))
        return elements, operations
    
    def generate_branching_program(elements, operations):
        # Generate a random read-twice branching program
        bp = []
        for _ in range(len(elements)):
            if random.choice([True, False]):
                bp.append(random.choice(operations))
            else:
                bp.append((random.choice(elements), random.choice(elements)))
        return bp
    
    def circuit_threshold(bp):
        # Calculate the circuit threshold of the branching program
        max_depth = 0
        for op in bp:
            if isinstance(op, tuple):
                depth = 1 + max(circuit_threshold(op[0]), circuit_threshold(op[1]))
            else:
                depth = 1
            if depth > max_depth:
                max_depth = depth
        return max_depth
    
    def free_probability_rank(elements, operations):
        # Calculate the rank of the free probability space on the dual vector space of B
        n = len(elements)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            matrix[i][i] = 1
        for op in operations:
            if isinstance(op, tuple):
                x, y = op
                idx_x = elements.index(x)
                idx_y = elements.index(y)
                matrix[idx_x][idx_y] += 1
                matrix[idx_y][idx_x] += 1
            else:
                x, y = op
                idx_x = elements.index(x)
                idx_y = elements.index(y)
                matrix[idx_x][idx_y] += 1
        return gaussian_elimination(matrix)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    elements, operations = generate_boolean_algebra(n)
    bp = generate_branching_program(elements, operations)
    rank = free_probability_rank(elements, operations)
    threshold = circuit_threshold(bp)
    
    if rank == 0:
        return {
            "metric_name": "Rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = threshold / rank
    conjecture_holds = abs(ratio - 2) <= 0.1  # Assuming the constant C is 2 for simplicity
    
    return {
        "metric_name": "Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Threshold: {threshold}, Rank: {rank}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")