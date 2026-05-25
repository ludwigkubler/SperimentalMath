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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        pivot = A[i][i]
        if pivot == 0:
            # Find a non-zero pivot in the column
            for k in range(i+1, n):
                if A[k][i] != 0:
                    A[i], A[k] = A[k], A[i]
                    pivot = A[i][i]
                    break
        if pivot == 0:
            # No non-zero pivot found, skip this column
            continue
        for j in range(n):
            if j != i:
                factor = A[j][i] / pivot
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def spectral_radius(A):
    n = len(A)
    eigenvalues = []
    for _ in range(10):  # Power iteration method
        x = [random.random() for _ in range(n)]
        x_norm = sum(x[i]**2 for i in range(n))**0.5
        x = [x_i / x_norm for x_i in x]
        Ax = [sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]
        lambda_k = sum(Ax[i] * x[i] for i in range(n))
        eigenvalues.append(lambda_k)
    return max(eigenvalues)

def generate_circuit(depth, size):
    circuit = []
    for _ in range(size):
        gate = random.choice(['AND', 'OR'])
        if gate == 'AND':
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, depth))]
        else:
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, depth))]
        circuit.append((gate, inputs))
    return circuit

def coxeter_group_action(circuit):
    n = len(circuit)
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                A[i][j] = 1
            elif abs(i - j) == 1:
                A[i][j] = -1
    return A

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Test 5 instances per size
            circuit = generate_circuit(n, n)
            A = coxeter_group_action(circuit)
            try:
                spectral_rad = spectral_radius(A)
                sigma_C = len(circuit)  # Assuming depth is the number of gates
                if spectral_rad < sigma_C / math.log(n):
                    conjecture_holds = False
                    counterexample = f"Depth {sigma_C}, Size {n}"
                    break
            except ZeroDivisionError:
                continue
            total_metric_value += spectral_rad
            instances_tested += 1

    return {
        "metric_name": "Spectral Radius",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 53))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")