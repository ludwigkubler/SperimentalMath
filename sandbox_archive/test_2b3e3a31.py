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
    
    def spectral_radius(matrix):
        n = len(matrix)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        eigenvalues = power_method(matrix, identity, n, max_iter=1000)
        return max(abs(e) for e in eigenvalues)

    def power_method(A, v0, n, max_iter):
        v = v0
        for _ in range(max_iter):
            v = matrix_multiply(A, v)
            norm = sum(x**2 for x in v)**0.5
            v = [x / norm for x in v]
        return v

    def matrix_multiply(A, B):
        n = len(A)
        result = [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        return result

    def generate_circuit(depth: int, size: int):
        if depth == 1:
            return [random.choice([0, 1])]
        else:
            sub_depth = random.randint(1, depth - 1)
            sub_size = random.randint(1, size // 2)
            left = generate_circuit(sub_depth, sub_size)
            right = generate_circuit(depth - sub_depth, size - sub_size)
            return [random.choice([0, 1]) if i == 0 else (left[i] + right[i]) % 2 for i in range(size)]

    def is_ac0_parity(circuit):
        return all(x in {0, 1} for x in circuit)

    def depth_of_circuit(circuit):
        if len(circuit) == 1:
            return 1
        else:
            left_depth = depth_of_circuit(circuit[:len(circuit)//2])
            right_depth = depth_of_circuit(circuit[len(circuit)//2:])
            return max(left_depth, right_depth) + 1

    def size_of_circuit(circuit):
        return len(circuit)

    n = random.randint(5, 40)
    circuit = generate_circuit(n, n)
    
    if not is_ac0_parity(circuit):
        return {
            "metric_name": "spectral_radius",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "not_ac0_parity"
        }

    depth = depth_of_circuit(circuit)
    size = size_of_circuit(circuit)

    sigma_C = depth
    spectral_rad = spectral_radius([[circuit[i]] for i in range(size)])
    
    conjecture_holds = spectral_rad >= sigma_C / math.log(n)
    counterexample = "" if conjecture_holds else f"depth={depth}, size={size}, sigma_C={sigma_C}, spectral_rad={spectral_rad}"
    
    return {
        "metric_name": "spectral_radius",
        "metric_value": spectral_rad,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r['metric_value'] for r in results) / len(results)
    std_dev = (sum((r['metric_value'] - mean)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]['counterexample']}\" first_failing_seed={first_failing_seed}")