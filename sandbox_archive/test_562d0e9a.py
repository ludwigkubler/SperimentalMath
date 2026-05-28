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
    
    def generate_xor_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def construct_symmetric_function(circuit):
        n = len(circuit)
        coeffs = [random.uniform(-1, 1) for _ in range(2**n)]
        symmetric_function = {}
        for i in range(2**n):
            binary_rep = f"{i:0{n}b}"
            if all(circuit[j] == int(binary_rep[j]) for j in range(n)):
                symmetric_function[binary_rep] = coeffs[i]
        return symmetric_function
    
    def hessian_matrix(symmetric_function, n):
        H = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            binary_rep_i = f"{i:0{n}b}"
            for j in range(2**n):
                binary_rep_j = f"{j:0{n}b}"
                if binary_rep_i != binary_rep_j:
                    H[i][j] = 0
                else:
                    count = sum(1 for k in range(n) if binary_rep_i[k] == '1')
                    H[i][j] = math.comb(count, 2)
        return H
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if all(matrix[j][i] == 0 for j in range(i, m)):
                continue
            pivot_row = i
            while matrix[pivot_row][i] == 0:
                pivot_row += 1
                if pivot_row == m:
                    return rank
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            for j in range(i + 1, m):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
            rank += 1
        return rank
    
    def max_weight(symmetric_function, n):
        weights = []
        for i in range(2**n):
            binary_rep = f"{i:0{n}b}"
            weight = sum(abs(symmetric_function[binary_rep]) * int(binary_rep[j]) for j in range(n))
            weights.append(weight)
        return max(weights)
    
    n = random.randint(5, 40)
    circuit = generate_xor_circuit(n)
    symmetric_function = construct_symmetric_function(circuit)
    H = hessian_matrix(symmetric_function, n)
    rank = matrix_rank(H)
    weight = max_weight(symmetric_function, n)
    
    c = 1.0  # Absolute constant
    threshold = c * (n / len(circuit))**(1/4)
    
    conjecture_holds = rank >= threshold
    counterexample = "" if conjecture_holds else f"Rank {rank} < {threshold}"
    
    return {
        "metric_name": "Rank of Hessian",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank < threshold\" first_failing_seed={first_failing_seed}")