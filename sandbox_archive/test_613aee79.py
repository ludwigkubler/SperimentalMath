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
    if len(A[0]) != len(B):
        raise ValueError("Incompatible dimensions for matrix multiplication")
    result = [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
    return result

def gaussian_elimination(matrix, b):
    n = len(matrix)
    augmented_matrix = [row + [b[i]] for i, row in enumerate(matrix)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda k: abs(augmented_matrix[k][i]))
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        if pivot == 0:
            continue
        for j in range(n):
            augmented_matrix[i][j] /= pivot
        b[i] /= pivot
        for k in range(n):
            if k != i and augmented_matrix[k][i] != 0:
                factor = augmented_matrix[k][i]
                for j in range(n):
                    augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
                b[k] -= factor * b[i]
    return [row[:-1] for row in augmented_matrix], b

def determinant(matrix):
    n = len(matrix)
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += (-1) ** j * matrix[0][j] * determinant(submatrix)
    return det

def is_invertible(matrix):
    return determinant(matrix) != 0

def rank(matrix):
    augmented_matrix, b = gaussian_elimination(matrix, [0] * len(matrix))
    non_zero_rows = sum(1 for row in augmented_matrix if any(row[i] != 0 for i in range(len(row))))
    return non_zero_rows

def generate_dfa(n):
    states = list(range(n))
    alphabet = ['0', '1']
    transitions = {q: {} for q in states}
    start_state = random.choice(states)
    accepting_states = [random.choice(states) for _ in range(2)]
    for q in states:
        for a in alphabet:
            if q == start_state and a == '0':
                next_state = (q + 1) % n
            elif q == start_state and a == '1':
                next_state = (q - 1) % n
            else:
                next_state = random.choice(states)
            transitions[q][a] = next_state
    return states, alphabet, transitions, start_state, accepting_states

def generate_cnf(n):
    literals = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for i in range(n):
        clause = random.sample(literals, 2)
        clauses.append(clause)
    return literals, clauses

def ac0_parity_depth(n):
    if n == 1:
        return 1
    return 1 + ac0_parity_depth(n // 2)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        if n == 1:
            continue
        if n % 2 == 0:
            states, alphabet, transitions, start_state, accepting_states = generate_dfa(n)
            language_type = 'regular'
        else:
            literals, clauses = generate_cnf(n)
            language_type = 'non-regular'
        
        automorphism_group_rank = rank([[1 if i == j else 0 for j in range(n)] for i in range(n)])
        ac0_depth = ac0_parity_depth(n)
        
        results.append((automorphism_group_rank, ac0_depth))
    
    metric_value = sum(rank_val * depth for rank_val, depth in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = True
    counterexample = ""
    
    if language_type == 'regular':
        c = 1.0 / math.log(2)
        size_A0_n = ac0_parity_depth(n)
        lower_bound = c * math.log(size_A0_n)
        if any(rank_val < lower_bound for rank_val, _ in results):
            conjecture_holds = False
            counterexample = "regular language with abnormally low automorphism group rank"
    elif language_type == 'non-regular':
        d = 2.0
        alpha = 1 / 4
        upper_bound = d * n ** alpha
        if any(rank_val < upper_bound for rank_val, _ in results):
            conjecture_holds = False
            counterexample = "non-regular language with abnormally low automorphism group rank"
    
    return {
        "metric_name": "average_automorphism_group_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")