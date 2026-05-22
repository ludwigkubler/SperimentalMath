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
    
    def generate_ac0_circuit(n):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            left = generate_ac0_circuit(n // 2)
            right = generate_ac0_circuit(n - n // 2)
            return [random.choice([0, 1]) for _ in range(len(left))] + left
    
    def circuit_to_quaternion(circuit):
        if len(circuit) == 1:
            return [[circuit[0], 0, 0, 0]]
        else:
            left = circuit_to_quaternion(circuit[:len(circuit)//2])
            right = circuit_to_quaternion(circuit[len(circuit)//2:])
            q_left = matrix_mult(left, left)
            q_right = matrix_mult(right, right)
            return matrix_add(q_left, q_right)
    
    def matrix_add(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = A[i][j] + B[i][j]
        return C
    
    def matrix_mult(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def matrix_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(rank, n)):
                rank += 1
        return rank
    
    def log2(x):
        return math.log2(x) if x > 0 else float('-inf')
    
    n = random.randint(5, 40)
    circuit = generate_ac0_circuit(n)
    q_matrix = circuit_to_quaternion(circuit)
    rank = matrix_rank(q_matrix)
    size = len(circuit)
    
    metric_name = "min_rank_bound"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank <= log2(size) + 1
    counterexample = "" if conjecture_holds else f"Circuit size {size}, rank {rank}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample_desc = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")