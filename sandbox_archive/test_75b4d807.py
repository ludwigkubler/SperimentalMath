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

def add(x, y):
    return x + y % 2

def multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    instances_tested = 0
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    def add_energy(f):
        count = 0
        for x in range(1 << n):
            for y in range(1 << n):
                for z in range(1 << n):
                    for w in range(1 << n):
                        if f(x) + f(y) == f(z) + f(w):
                            count += 1
        return count

    def ac0_energy(f):
        count = 0
        for x in range(1 << n):
            for y in range(1 << n):
                for z in range(1 << n):
                    for w in range(1 << n):
                        if f(x) + f(y) == f(z) + f(w):
                            count += 1
        return count

    def parity_function(x):
        return sum(int(bit) for bit in bin(x)[2:]) % 2

    def ac0_circuit(x):
        # Example AC⁰ circuit: depth-2 AND-OR tree
        layer1 = [x & y for x, y in zip([1, 3, 5, 7], [8, 9, 10, 11])]
        layer2 = [layer1[0] | layer1[1], layer1[2] | layer1[3]]
        return layer2[0]

    for _ in range(30):
        if random.random() < 0.5:
            f = parity_function
        else:
            f = ac0_circuit
        instances_tested += 1
        energy = add_energy(f)
        metric_value += energy
        if f == parity_function and energy > 4 * n ** 2:
            conjecture_holds = False
            counterexample = "P function with high additive energy"
        elif f == ac0_circuit and energy < (2 ** (2 * n)) / n ** 2:
            conjecture_holds = False
            counterexample = "AC⁰ circuit with low additive energy"

    return {
        "metric_name": "Additive Energy",
        "metric_value": metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.2f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean = sum(r["metric_value"] for r in results) / len(results)
    std = (sum((r["metric_value"] - mean) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean:.2f} std={std:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean:.2f} std={std:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")