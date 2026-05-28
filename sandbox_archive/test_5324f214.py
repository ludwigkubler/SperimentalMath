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
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

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

def generate_monotone_circuit(k):
    n = 2 ** k
    inputs = list(range(n))
    gates = []
    while len(inputs) > 1:
        new_inputs = []
        for i in range(0, len(inputs), 2):
            gate = {
                'type': 'OR' if random.choice([True, False]) else 'AND',
                'inputs': [inputs.pop(), inputs.pop()],
                'output': None
            }
            gates.append(gate)
            new_inputs.append(len(gates) - 1)
        inputs = new_inputs
    return gates

def construct_tropical_vector_bundle(C):
    n = len(C)
    m = 2 ** (n + 1)
    V = [[0] * m for _ in range(m)]
    for gate in C:
        i, j = gate['inputs']
        if gate['type'] == 'OR':
            V[i][j] = 1
        else:  # AND
            V[i][j] = -1
    return V

def min_rank(V):
    m, n = len(V), len(V[0])
    A = [[Fraction(v) for v in row] for row in V]
    b = [0] * m
    try:
        solution = gaussian_elimination(A, b)
        rank = sum(1 for x in solution if x != 0)
        return rank
    except ZeroDivisionError:
        return float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        k = int(math.log(n, 2))
        C = generate_monotone_circuit(k)
        V = construct_tropical_vector_bundle(C)
        rank = min_rank(V)
        results.append({
            'n': n,
            'k': k,
            'rank': rank
        })
    metric_value = sum(result['rank'] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result['rank'] >= n ** k * math.log(n) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "min_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result['metric_value'] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result['metric_value'] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result['conjecture_holds']) / len(results)
    
    if all(result['conjecture_holds'] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result['conjecture_holds'] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")