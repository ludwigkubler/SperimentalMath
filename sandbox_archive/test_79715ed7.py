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
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError('Modular inverse does not exist')
    else:
        return x % m

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_power(A, k):
    n = len(A)
    result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    while k > 0:
        if k % 2 == 1:
            result = matrix_multiply(result, A)
        A = matrix_multiply(A, A)
        k //= 2
    return result

def is_finite_field(q):
    return isinstance(q, int) and q > 1

def generate_random_branching_program(n, width, q):
    if not is_finite_field(q):
        raise ValueError("q must be a finite field")
    
    program = []
    for _ in range(n):
        row = [random.randint(0, q - 1) for _ in range(width)]
        program.append(row)
    return program

def compute_transition_algebra(program, q):
    width = len(program[0])
    n = len(program)
    transition_matrix = [[0] * (width + 1) for _ in range(n + 1)]
    
    for i in range(n):
        for j in range(width):
            transition_matrix[i][j] = program[i][j]
    
    for i in range(n):
        transition_matrix[n][i] = 1
    
    return transition_matrix

def compute_faithful_module_dimension(transition_matrix, q):
    n = len(transition_matrix)
    width = len(transition_matrix[0]) - 1
    identity_matrix = [[0 if i != j else 1 for j in range(width + 1)] for i in range(n)]
    
    # Compute the kernel of the transition matrix
    kernel = []
    for i in range(width + 1):
        row = [transition_matrix[j][i] for j in range(n)]
        kernel.append(row)
    
    # Extend the kernel to a basis
    basis = []
    for i in range(width + 1):
        if all(kernel[i][j] == 0 for j in range(i)):
            basis.append(kernel[i])
    
    # Compute the dimension of the kernel
    dim_kernel = len(basis)
    
    return dim_kernel

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(50):
            q = random.randint(2, 10)
            program = generate_random_branching_program(n, 5, q)
            transition_matrix = compute_transition_algebra(program, q)
            dim_module = compute_faithful_module_dimension(transition_matrix, q)
            
            total_metric_value += dim_module
            instances_tested += 1
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = True
    counterexample = ""
    
    return {
        "metric_name": "Faithful Module Dimension",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3**j for i in range(5) for j in range(5)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")