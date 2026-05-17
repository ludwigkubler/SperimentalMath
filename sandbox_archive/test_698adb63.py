# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from fractions import Fraction

def generate_random_acc0_circuit(n, s, m=6):
    if s < 3:
        return [['AND', [('AND', [i]) for i in range(n)]]]
    circuit = []
    for _ in range(s):
        if random.random() < 0.5:
            inputs = random.sample(range(n), random.randint(1, n))
            circuit.append(['AND', [('AND', [i]) for i in inputs]])
        else:
            inputs = random.sample(range(n), random.randint(1, n))
            circuit.append(['MOD', m, [('AND', [i]) for i in inputs]])
    return circuit

def evaluate_circuit(circuit, x):
    if isinstance(circuit, list):
        if circuit[0] == 'AND':
            return all(evaluate_circuit(sub, x) for sub in circuit[1])
        elif circuit[0] == 'MOD':
            m = circuit[1]
            return sum(evaluate_circuit(sub, x) for sub in circuit[2]) % m == 0
    elif isinstance(circuit, tuple):
        if circuit[0] == 'AND':
            return x[circuit[1]]
    return False

def walsh_hadamard_transform(circuit, n):
    f_hat = {}
    for alpha in itertools.product([-1, 1], repeat=n):
        f_hat[alpha] = sum(evaluate_circuit(circuit, x) * math.prod(alpha[i] * x[i] for i in range(n))
                          for x in itertools.product([-1, 1], repeat=n))
    return f_hat

def build_linear_system(f_hat, n):
    system = []
    for alpha in itertools.product([-1, 1], repeat=n):
        row = []
        for i in range(n):
            for j in range(n):
                if i == j:
                    row.append(Fraction(f_hat[alpha] * alpha[i], 1))
                else:
                    row.append(Fraction(0, 1))
        system.append(row)
    return system

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        if matrix[i][i] == 0:
            for j in range(i+1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
        if matrix[i][i] == 0:
            continue
        for j in range(i+1, n):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(i, n):
                matrix[j][k] -= factor * matrix[i][k]
    rank = sum(1 for i in range(n) if any(matrix[i][j] != 0 for j in range(n)))
    return n - rank

def run_trial(seed):
    random.seed(seed)
    n = random.choice([4, 5, 6, 7])
    s = random.choice([3, 8, 20, 50])
    circuit = generate_random_acc0_circuit(n, s)
    f_hat = walsh_hadamard_transform(circuit, n)
    system = build_linear_system(f_hat, n)
    gamma = gaussian_elimination(system)
    slack = gamma - (n**2 - 10*s)
    conjecture_holds = slack >= 0
    counterexample = f"n={n}, s={s}, circuit={circuit}" if not conjecture_holds else ""
    return {
        "metric_name": "slack",
        "metric_value": slack,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if not r["conjecture_holds"])]
        counterexample = results[next(i for i, r in enumerate(results) if not r["conjecture_holds"])]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")