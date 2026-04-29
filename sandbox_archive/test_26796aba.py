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
    
    def generate_read_twice_bp(n):
        states = [0, 1]
        transitions = {i: {} for i in states}
        for i in states:
            for j in range(n):
                if random.choice([True, False]):
                    transitions[i][j] = (random.choice(states), j + 1)
                else:
                    transitions[i][j] = (random.choice(states), j - 1)
        return transitions
    
    def generate_trivial_bp(n):
        states = [0]
        transitions = {i: {} for i in states}
        for i in states:
            for j in range(n):
                transitions[i][j] = (i, (j + 1) % n)
        return transitions
    
    def matrix_multiply(A, B):
        m, k = len(A), len(B[0])
        result = [[0] * k for _ in range(m)]
        for i in range(m):
            for j in range(k):
                for l in range(len(B)):
                    result[i][j] += A[i][l] * B[l][j]
        return result
    
    def gaussian_elimination(A, b):
        n = len(A)
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
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
        return x
    
    def r_transform(M):
        n = len(M)
        I = [[int(i == j) for j in range(n)] for i in range(n)]
        M_inv = gaussian_elimination([[M[i][j] if i != j else 1 for j in range(n)] for i in range(n)], [0] * n)
        return sum(M_inv[i][j] * I[j][i] for i in range(n) for j in range(n))
    
    def free_entropy(M):
        return -math.log(r_transform(M))
    
    n = 40
    read_twice_bp = generate_read_twice_bp(n)
    trivial_bp = generate_trivial_bp(n)
    
    def transition_matrix(bp):
        m = len(bp[0])
        M = [[0] * m for _ in range(m)]
        for i in bp:
            for j in range(m):
                if j in bp[i]:
                    M[i][bp[i][j]] += 1
        return M
    
    read_twice_matrix = transition_matrix(read_twice_bp)
    trivial_matrix = transition_matrix(trivial_bp)
    
    read_twice_entropy = free_entropy(read_twice_matrix)
    trivial_entropy = free_entropy(trivial_matrix)
    
    metric_name = "Free Entropy Gap"
    metric_value = abs(read_twice_entropy - math.log(n))
    instances_tested = 1
    conjecture_holds = (read_twice_entropy >= math.log(n)) and (trivial_entropy <= n**2)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")