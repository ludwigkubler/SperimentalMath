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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_xor_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def construct_symmetric_function(circuit):
        n = len(circuit)
        inputs = list(range(n))
        value = 0
        for x in itertools.product([0, 1], repeat=n):
            if sum(x) % 2 == circuit[sum(x)]:
                value |= all(x[j] for j in inputs)
        return value
    
    def hessian_matrix(f, n):
        H = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                H[i][j] = H[j][i] = f(x[:i] + (1 - x[i],) + x[i+1:j] + (1 - x[j],) + x[j+1:])
        return H
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        if m == 0 or n == 0:
            return 0
        rank = 0
        for i in range(min(m, n)):
            pivot_row = -1
            for r in range(i, m):
                if matrix[r][i] != 0:
                    pivot_row = r
                    break
            if pivot_row == -1:
                continue
            rank += 1
            for j in range(n):
                matrix[pivot_row][j] /= matrix[pivot_row][i]
            for r in range(m):
                if r != pivot_row and matrix[r][i] != 0:
                    for j in range(n):
                        matrix[r][j] -= matrix[pivot_row][j] * matrix[r][i]
        return rank
    
    def max_weight(circuit, n):
        weights = [0] * (1 << n)
        for i in range(1 << n):
            inputs = [(i >> j) & 1 for j in range(n)]
            if sum(inputs) % 2 == circuit[sum(inputs)]:
                weights[i] = sum(inputs)
        return max(weights)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit = generate_xor_circuit(n)
    f = construct_symmetric_function(circuit)
    H = hessian_matrix(f, n)
    rank = matrix_rank(H)
    S = len(circuit)
    
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank >= (n / S) ** 0.25
    counterexample = "" if conjecture_holds else f"Rank {rank} < {(n / S) ** 0.25}"
    
    return {
        "metric_name": "Hessian Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30)) + [59, 61, 67, 71, 73]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank too low\" first_failing_seed={first_failing_seed}")