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
    return abs(a * b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError('Modular inverse does not exist')
    else:
        return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    adj = [[0 for _ in range(n)] for _ in range(n)]
    det = determinant(matrix) % mod
    if det == 0:
        raise ValueError('Matrix is not invertible')
    inv_det = mod_inverse(det, mod)
    for i in range(n):
        for j in range(n):
            adj[j][i] = ((-1)**(i+j) * minor(matrix, i, j)) % mod
    return matrix_mod_mul(adj, inv_det, mod)

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for c in range(n):
        det += ((-1)**c) * matrix[0][c] * determinant([row[:c] + row[c+1:] for row in matrix[1:]])
    return det

def minor(matrix, i, j):
    return [row[:j] + row[j+1:] for row in matrix[:i] + matrix[i+1:]]

def matrix_mod_mul(A, B, mod):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

def generate_generators(q, n):
    generators = []
    for i in range(1, q):
        if gcd(i, q) == 1:
            generators.append(i)
        if len(generators) >= n:
            break
    return generators[:n]

def construct_drinfeld_modular_curve(f, q):
    n = len(f)
    generators = generate_generators(q, n)
    curve = []
    for x in range(q):
        y = 0
        for i in range(n):
            y += f[i] * (x ** i) % q
        curve.append((x, y))
    return curve

def geometric_entropy(curve):
    n = len(curve)
    entropy = 0
    for x, y in curve:
        if y != 0:
            entropy -= math.log2(1 / n)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    q = random.randint(5, 100)
    f = [random.randint(0, q-1) for _ in range(random.randint(5, 40))]
    curve = construct_drinfeld_modular_curve(f, q)
    entropy = geometric_entropy(curve)
    return {
        "metric_name": "geometric_entropy",
        "metric_value": entropy,
        "instances_tested": len(curve),
        "conjecture_holds": entropy <= math.log(len(f)) * math.log(math.log(len(f))),
        "counterexample": "" if entropy <= math.log(len(f)) * math.log(math.log(len(f))) else f"Entropy {entropy} exceeds bound"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    std_entropy = math.sqrt(sum((r["metric_value"] - mean_entropy) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy:.4f} std={std_entropy:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Entropy exceeds bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")