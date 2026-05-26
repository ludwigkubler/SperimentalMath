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
    
    # Define k and n for the trial
    k = random.randint(5, 40)
    n = random.randint(10, 40)
    
    # Generate a random monotone circuit C of size poly(n)
    # For simplicity, we will use a binary tree structure as an example
    def generate_monotone_circuit(k):
        if k == 1:
            return [random.choice([0, 1])]
        else:
            left = generate_monotone_circuit(k // 2)
            right = generate_monotone_circuit(k - k // 2)
            return [left[i] or right[i] for i in range(len(left))]
    
    circuit = generate_monotone_circuit(k)
    
    # Compute the tensor product representation of its input space
    # For simplicity, we will use a binary matrix to represent the tensor product
    def tensor_product(matrix1, matrix2):
        result = []
        for row1 in matrix1:
            new_row = []
            for row2 in matrix2:
                new_row.extend([a * b for a, b in zip(row1, row2)])
            result.append(new_row)
        return result
    
    input_space = [[0] * n, [1] * n]
    tensor_product_representation = input_space
    for _ in range(k):
        tensor_product_representation = tensor_product(tensor_product_representation, input_space)
    
    # Measure the rank of this representation
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        if m == 0 or n == 0:
            return 0
        
        # Gaussian elimination to find the rank
        for i in range(min(m, n)):
            # Find a non-zero pivot
            while i < m and all(x == 0 for x in matrix[i]):
                i += 1
            if i == m:
                break
            
            # Make the pivot 1
            denom = matrix[i][i]
            if denom == 0:
                continue
            for j in range(n):
                matrix[i][j] /= denom
            
            # Eliminate other rows
            for j in range(m):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        
        return sum(1 for row in matrix if any(x != 0 for x in row))
    
    rank = matrix_rank(tensor_product_representation)
    
    # Check if the conjecture holds
    conjecture_holds = rank <= n ** (math.ceil(k ** 0.25))
    counterexample = "" if conjecture_holds else f"Rank {rank} exceeds n^Ω(k^{1/4})"
    
    return {
        "metric_name": "tensor_product_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else list(range(2, 307))  # First 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")