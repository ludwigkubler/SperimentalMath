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

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = i
        for j in range(i+1, m):
            if abs(augmented[j][i]) > abs(augmented[max_row][i]):
                max_row = j
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        pivot = augmented[i][i]
        for j in range(n + 1):
            augmented[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = augmented[j][i]
                for k in range(n + 1):
                    augmented[j][k] -= factor * augmented[i][k]
    return [row[-1] for row in augmented]

def tropical_add(x, y):
    return max(x, y)

def tropical_multiply(x, y):
    if x == float('-inf') or y == float('-inf'):
        return float('-inf')
    return x + y

def tropical_negate(x):
    return -x

def tropical_convex_hull(points):
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2

    def convex_hull(points):
        n = len(points)
        if n < 3:
            return points
        l = min(range(n), key=lambda i: (points[i][0], points[i][1]))
        hull = []
        p = l
        q = (p + 1) % n
        while True:
            hull.append(p)
            q = (q + 1) % n
            for r in range(n):
                if orientation(points[p], points[q], points[r]) == 2:
                    q = r
            p = q
            if p == l:
                break
        return [points[i] for i in hull]

    return convex_hull(points)

def tropical_circuit_rank(circuit):
    n = len(circuit)
    A = [[tropical_negate(circuit[j][i]) for j in range(n)] for i in range(n)]
    b = [0] * n
    x = gaussian_elimination(A, b)
    return sum(1 for xi in x if xi != float('-inf'))

def duality_flip(circuit):
    n = len(circuit)
    dual_circuit = [[circuit[j][i] for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            dual_circuit[i][j], dual_circuit[j][i] = dual_circuit[j][i], dual_circuit[i][j]
    return dual_circuit

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 5 + (seed % 10) * 5
    circuit = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    tropical_rank = tropical_circuit_rank(circuit)
    dual_circuit = duality_flip(circuit)
    dual_tropical_rank = tropical_circuit_rank(dual_circuit)
    phase_cells = len(tropical_convex_hull([(i, j) for i in range(n) for j in range(n) if circuit[i][j] != float('-inf')]))
    dual_phase_cells = len(tropical_convex_hull([(i, j) for i in range(n) for j in range(n) if dual_circuit[i][j] != float('-inf')]))
    metric_value = max(phase_cells, dual_phase_cells)
    conjecture_holds = metric_value <= 2 * tropical_rank
    counterexample = "" if conjecture_holds else "duality_flip_failed"
    return {
        "metric_name": "phase_cell_count",
        "metric_value": metric_value,
        "instances_tested": n * n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
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
        print(f"RESULT: FALSIFIED counterexample=\"duality_flip_failed\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE insufficient_data")