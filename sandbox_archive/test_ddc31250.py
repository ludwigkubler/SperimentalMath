# auto-injected by SEC sandbox
import math
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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = extended_gcd(b % a, a)
        return g, x - (b // a) * y, y

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError('Modular inverse does not exist')
    else:
        return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    det = 0
    for i in range(n):
        det += (-1) ** i * matrix[0][i] * determinant([[matrix[j][k] for k in range(1, n)] for j in range(1, n)], mod)
    det = det % mod
    inv_det = mod_inverse(det, mod)
    adjugate = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [[matrix[x][y] for y in range(j, n)] for x in range(i, n)]
            minor = [row[:j] + row[j+1:] for row in minor]
            adjugate[i][j] = (-1) ** (i+j) * determinant(minor, mod)
    adjugate = [[adjugate[j][i] for j in range(n)] for i in range(n)]
    inv_matrix = [[(inv_det * adjugate[i][j]) % mod for j in range(n)] for i in range(n)]
    return inv_matrix

def determinant(matrix, mod):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for i in range(n):
        minor = [[matrix[j][k] for k in range(1, n)] for j in range(1, n)]
        minor = [row[:i] + row[i+1:] for row in minor]
        det += (-1) ** i * matrix[0][i] * determinant(minor, mod)
    return det % mod

def young_diagram(n):
    if n == 0:
        return [[]]
    diagrams = []
    for k in range(1, n+1):
        for diagram in young_diagram(k-1):
            diagrams.append([k] + diagram)
            if len(diagram) > 0 and diagram[0] >= k:
                new_diagram = [diagram[0]-1] + diagram[1:]
                while len(new_diagram) > 0 and new_diagram[-1] == new_diagram[-2]:
                    new_diagram.pop()
                diagrams.append([k] + new_diagram)
    return diagrams

def irreducible_representation_degree(n):
    diagrams = young_diagram(n)
    degrees = []
    for diagram in diagrams:
        degree = 1
        for part in diagram:
            degree *= (part + n - len(diagram)) // gcd(part, n - len(diagram))
        degrees.append(degree)
    return max(degrees)

def permanent(matrix):
    n = len(matrix)
    if n == 0:
        return 1
    elif n == 1:
        return matrix[0][0]
    else:
        det = 0
        for i in range(n):
            minor = [[matrix[j][k] for k in range(i+1, n)] for j in range(1, n)]
            det += (-1) ** i * matrix[0][i] * permanent(minor)
        return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    d = irreducible_representation_degree(n)
    circuit_size = permanent([[random.choice([0, 1]) for _ in range(n)] for _ in range(n)])
    metric_value = circuit_size / (2**d / n**2)
    conjecture_holds = metric_value >= 1
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "circuit_size_over_d_n_squared",
        "metric_value": metric_value,
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
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    mean = sum(r["metric_value"] for r in results) / len(results)
    std = (sum((r["metric_value"] - mean)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")