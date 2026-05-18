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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        # Find pivot
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below pivot
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    return A

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_norm(A, norm_type='frobenius'):
    if norm_type == 'frobenius':
        sum_of_squares = sum(sum(abs(x)**2 for x in row) for row in A)
        return math.sqrt(sum_of_squares)
    elif norm_type == 'op':
        m, n = len(A), len(A[0])
        A_transpose = [[A[j][i] for j in range(m)] for i in range(n)]
        A_transpose_norm = matrix_norm(A_transpose, 'frobenius')
        return A_transpose_norm
    else:
        raise ValueError("Unsupported norm type")

def vec(matrix):
    return [x for row in matrix for x in row]

def layer_difference_stack(T0, T1):
    return [vec(T1[i] - T0[i]) for i in range(len(T0))]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(3, 9)
    w = random.choice([3, 4, 5, 6])
    L = 4 * n
    
    # Generate random RT-BP
    T0 = [[random.randint(0, 1) for _ in range(w)] for _ in range(w)]
    T1 = [[random.randint(0, 1) for _ in range(w)] for _ in range(w)]
    
    D = layer_difference_stack(T0, T1)
    norm_frobenius = matrix_norm(D, 'frobenius')
    norm_op = matrix_norm(D, 'op')
    
    s_P = w * L
    rho_P = math.log2(norm_frobenius**2 / norm_op**2) if norm_op != 0 else 0
    
    # Check upper bound for random RT-BP
    upper_bound_holds = rho_P <= 2 * math.log2(s_P + 1)
    
    # Construct canonical exponential-width RT-BP for IP_2
    if n <= 9:
        states = [(0, '')]
        transitions = {}
        for i in range(n):
            new_states = []
            for state, prefix in states:
                for bit in [0, 1]:
                    new_state = (state ^ bit, prefix + str(bit))
                    transitions[(state, bit)] = new_state
                    new_states.append(new_state)
            states = new_states
        
        T_IP2 = [[transitions.get((i // w, i % w), 0) for _ in range(w)] for _ in range(w)]
        
        D_IP2 = layer_difference_stack(T_IP2, T_IP2)
        norm_frobenius_IP2 = matrix_norm(D_IP2, 'frobenius')
        norm_op_IP2 = matrix_norm(D_IP2, 'op')
        
        rho_P_IP2 = math.log2(norm_frobenius_IP2**2 / norm_op_IP2**2) if norm_op_IP2 != 0 else 0
        
        # Check lower bound for canonical IP_2 RT-BP
        lower_bound_holds = rho_P_IP2 >= n / 4
    
    else:
        upper_bound_holds = True
        lower_bound_holds = False
    
    return {
        "metric_name": "rho(P)",
        "metric_value": rho_P,
        "instances_tested": 1 if n <= 9 else 0,
        "conjecture_holds": upper_bound_holds and lower_bound_holds,
        "counterexample": "" if upper_bound_holds and lower_bound_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    if all(result["conjecture_holds"] for result in results):
        mean_rho = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")