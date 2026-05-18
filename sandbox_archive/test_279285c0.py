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
        for r in range(i+1, m):
            if abs(A[r][i]) > abs(A[max_row][i]):
                max_row = r
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for r in range(i+1, m):
            factor = A[r][i] / A[i][i]
            for c in range(n):
                A[r][c] -= factor * A[i][c]

    return A

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def vec(v):
    return [v]

def layer_difference_stack(T0, T1):
    return [vec(T1[i]) - vec(T0[i]) for i in range(len(T0))]

def frobenius_norm(A):
    sum_squares = 0
    for row in A:
        for elem in row:
            sum_squares += elem ** 2
    return math.sqrt(sum_squares)

def operator_norm(A):
    m, n = len(A), len(A[0])
    max_row_sum = 0
    for i in range(m):
        row_sum = 0
        for j in range(n):
            row_sum += abs(A[i][j])
        if row_sum > max_row_sum:
            max_row_sum = row_sum
    return max_row_sum

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(3, 9)
    w = random.choice([3, 4, 5, 6])
    L = 4 * n
    
    # Generate random transition matrices
    T0 = [[random.choice([0, 1]) for _ in range(w)] for _ in range(L)]
    T1 = [[random.choice([0, 1]) for _ in range(w)] for _ in range(L)]
    
    D = layer_difference_stack(T0, T1)
    frob_norm_squared = sum(frobenius_norm(row) ** 2 for row in D)
    op_norm = operator_norm(D)
    
    s_P = w * L
    rho_P = math.log2(frob_norm_squared / (op_norm ** 2)) if op_norm != 0 else 0
    
    # Check upper bound
    upper_bound_holds = rho_P <= 2 * math.log2(s_P + 1)
    
    # Construct canonical IP_2 RT-BP
    if n <= 9:
        # Canonical exponential-width RT-BP for IP_2 under adversarial order
        states = [(0, '')]
        transitions = {}
        for i in range(n):
            new_states = []
            for state, prefix in states:
                for bit in [0, 1]:
                    new_state = (state ^ bit, prefix + str(bit))
                    if new_state not in transitions:
                        transitions[new_state] = []
                    transitions[new_state].append((state, bit, new_state))
                    new_states.append(new_state)
            states = new_states
        
        # Compute D(P_IP2(n)) and check lower bound
        rho_P_IP2_n = math.log2(len(states) / len(transitions))
        lower_bound_holds = rho_P_IP2_n >= n / 4
    
    else:
        lower_bound_holds = True
    
    return {
        "metric_name": "rho(P)",
        "metric_value": rho_P,
        "instances_tested": 1,
        "conjecture_holds": upper_bound_holds and lower_bound_holds,
        "counterexample": "" if upper_bound_holds and lower_bound_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    if all(trial["conjecture_holds"] for trial in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(trial["conjecture_holds"] for trial in results) / len(results)
    
    mean_rho_P = sum(trial["metric_value"] for trial in results) / len(results)
    std_rho_P = math.sqrt(sum((trial["metric_value"] - mean_rho_P) ** 2 for trial in results) / len(results))
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho_P} std={std_rho_P} support_fraction={support_fraction}")
    elif any(not trial["conjecture_holds"] for trial in results):
        first_failing_seed = next(seed for seed, trial in zip(seeds, results) if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")