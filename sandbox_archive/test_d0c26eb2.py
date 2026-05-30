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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def evaluate(f, x):
    result = f[0]
    for i in range(1, len(f)):
        result ^= (x & (1 << (i - 1))) * f[i]
    return result

def is_linear(f):
    n = int(math.log2(len(f)))
    A = [[evaluate(f, x ^ y) for y in range(2**n)] for x in range(2**n)]
    b = [evaluate(f, x) for x in range(1, 2**n)]
    return gaussian_elimination(A, b)

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        if A[i][i] == 0:
            for j in range(i + 1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    b[i], b[j] = b[j], b[i]
                    break
            else:
                return False
        for j in range(n):
            if i == j:
                continue
            factor = -A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] += factor * A[i][k]
            b[j] += factor * b[i]
    for i in range(n):
        if A[i][i] == 0:
            return False
        b[i] /= A[i][i]
    return True

def count_representations(f):
    n = int(math.log2(len(f)))
    count = 0
    for F in range(1, 2**n + 1):
        if (F & (F - 1)) == 0:  # Check if F is a power of 2
            count += 1
    return count

def linear_representations(f):
    n = int(math.log2(len(f)))
    C_f = count_representations(f)
    Omega_f = min([len(circuit) for circuit in generate_circuits(n)])
    if Omega_f == 0:
        return 0
    ratio = (math.log(n + 1)**2 * C_f) / Omega_f
    return ratio

def generate_circuits(n):
    circuits = []
    for i in range(2**n):
        circuit = [i]
        x = i
        while True:
            if x == 0:
                break
            x ^= (x & -x)
            circuit.append(x)
        circuits.append(circuit)
    return circuits

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        C_f = linear_representations(f)
        Omega_f = min([len(circuit) for circuit in generate_circuits(n)])
        if Omega_f == 0:
            continue
        ratio = (math.log(n + 1)**2 * C_f) / Omega_f
        results.append(ratio)
    metric_value = sum(results) / len(results)
    conjecture_holds = all(0.5 <= r <= 2 for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "ratio",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if 0.5 <= r <= 2) / len(results)
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r < 0.5 or r > 2 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not (0.5 <= result <= 2))
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")