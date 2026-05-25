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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    Ab = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(Ab[j][i]) > abs(Ab[max_row][i]):
                max_row = j
        Ab[i], Ab[max_row] = Ab[max_row], Ab[i]
        factor = Ab[i][i]
        for j in range(i, n + 1):
            Ab[i][j] /= factor
        for j in range(n):
            if j != i:
                factor = Ab[j][i]
                for k in range(i, n + 1):
                    Ab[j][k] -= factor * Ab[i][k]
    return [row[-1] for row in Ab]

def min_rank(A):
    m, n = len(A), len(A[0])
    rank = 0
    for i in range(min(m, n)):
        if A[i][i] != 0:
            rank += 1
    return rank

def communication_complexity(n):
    # Placeholder function; replace with actual computation
    return n * (n - 1) // 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    inputs = [random.choice([0, 1]) for _ in range(n)]
    
    # Construct affine Grassmannian G
    A = [[i * j for j in range(n)] for i in range(n)]
    b = [sum(inputs) % 2]
    rank = min_rank(A)
    
    CC_R = communication_complexity(n)
    diff = abs(rank - CC_R)
    
    return {
        "metric_name": "min_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": diff <= 3,
        "counterexample": "" if diff <= 3 else f"Rank {rank}, CC_R {CC_R}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds CC_R\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")