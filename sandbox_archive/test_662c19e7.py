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
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    
    for i in range(n):
        max_row = i
        for j in range(i+1, m):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        pivot = augmented_matrix[i][i]
        for j in range(i, n+1):
            augmented_matrix[i][j] /= pivot
        
        for j in range(m):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, n+1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = augmented_matrix[i][-1]
        for j in range(i+1, n):
            x[i] -= augmented_matrix[i][j] * x[j]
    
    return x

def construct_quasi_group_representation(circuit):
    inputs = circuit['inputs']
    outputs = circuit['outputs']
    gates = circuit['gates']
    
    qg = {}
    for gate in gates:
        input_indices = [inputs.index(gate['input']) for gate in gate['inputs']]
        output_index = outputs.index(gate['output'])
        
        if (input_indices, output_index) not in qg:
            qg[(input_indices, output_index)] = (output_index, input_indices[output_index])
    
    return qg

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    circuit_size = n ** (2/3)
    depth = n ** (1/3)
    
    if circuit_size < 5 or depth < 5:
        return {
            "metric_name": "rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "sub-asymptotic n"
        }
    
    if circuit_size > 1000 or depth > 1000:
        return {
            "metric_name": "rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "budget_exceeded"
        }
    
    circuit = {
        'inputs': list(range(n)),
        'outputs': list(range(n)),
        'gates': []
    }
    
    for _ in range(int(circuit_size)):
        gate_type = random.choice(['AND', 'OR'])
        inputs = random.sample(range(n), 2)
        output = random.randint(0, n-1)
        
        circuit['gates'].append({
            'type': gate_type,
            'inputs': [{'input': input} for input in inputs],
            'output': output
        })
    
    qg = construct_quasi_group_representation(circuit)
    
    rank = len(qg)
    
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all('conjecture_holds' in r and r['conjecture_holds'] for r in results):
        mean_rank = sum(r['metric_value'] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}")
    elif any('conjecture_holds' in r and not r['conjecture_holds'] for r in results):
        first_failing_seed = next(r['seed'] for r in results if 'conjecture_holds' in r and not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"rank < log(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")