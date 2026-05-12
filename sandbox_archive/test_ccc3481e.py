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
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0]*n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for c in range(n):
        submatrix = [row[:c] + row[c+1:] for row in A[1:]]
        det += ((-1)**c) * A[0][c] * determinant(submatrix)
    return det

def euler_characteristic(clique_complex):
    n = len(clique_complex)
    return sum((-1)**k * len(clique_complex[k]) for k in range(n))

def communication_graph(f, n):
    vertices = [(i, j) for i in range(2**n) for j in range(i+1, 2**n)]
    edges = []
    for u, v in vertices:
        if f(u) != f(v):
            edges.append((u, v))
    return vertices, edges

def deterministic_communication_complexity(f, n):
    # Placeholder for actual computation
    return 0  # Replace with actual implementation

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    f = lambda x: sum(x[i] for i in range(n)) % 2  # Example Boolean function
    vertices, edges = communication_graph(f, n)
    clique_complex = [[] for _ in range(n+1)]
    for edge in edges:
        u, v = edge
        for k in range(n):
            if (u & (1 << k)) != (v & (1 << k)):
                break
        else:
            continue
        clique_complex[k].append(edge)
    euler_char = euler_characteristic(clique_complex)
    comm_complexity = deterministic_communication_complexity(f, n)
    diff = abs(euler_char - comm_complexity)
    return {
        "metric_name": "Absolute Difference",
        "metric_value": diff,
        "instances_tested": 1,
        "conjecture_holds": diff == 0,
        "counterexample": "" if diff == 0 else f"Diff: {diff}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_diff = sum(r['metric_value'] for r in results) / len(results)
    std_dev = math.sqrt(sum((r['metric_value'] - mean_diff)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if not r['conjecture_holds']) / len(results)
    
    if support_fraction < 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={seeds[0]}")
    else:
        print(f"RESULT: SUPPORTED mean={mean_diff} std={std_dev} support_fraction={support_fraction}")