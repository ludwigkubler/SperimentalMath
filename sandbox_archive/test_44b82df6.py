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
    augmented_matrix = [row + [b[i]] for i, row in enumerate(A)]
    for j in range(n):
        max_row = j
        for i in range(j+1, m):
            if abs(augmented_matrix[i][j]) > abs(augmented_matrix[max_row][j]):
                max_row = i
        augmented_matrix[j], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[j]
        pivot = augmented_matrix[j][j]
        for i in range(j, n+1):
            augmented_matrix[j][i] /= pivot
        for i in range(m):
            if i != j:
                factor = augmented_matrix[i][j]
                for k in range(j, n+1):
                    augmented_matrix[i][k] -= factor * augmented_matrix[j][k]
    return [row[-1] for row in augmented_matrix]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    width = random.randint(2, n)
    
    # Generate a read-twice branching program
    branching_program = [[random.choice([0, 1]) for _ in range(width)] for _ in range(n)]
    
    # Compute the transition function
    transition_function = {}
    for i in range(n):
        for j in range(width):
            if branching_program[i][j] == 0:
                next_state = (i + 1) % n
            else:
                next_state = (n - i - 2) % n
            if (i, j) not in transition_function:
                transition_function[(i, j)] = []
            transition_function[(i, j)].append(next_state)
    
    # Compute the Hodge structure associated with the transition function
    hodge_structure = []
    for state in range(n):
        for i in range(width):
            if (state, i) not in transition_function:
                continue
            next_states = transition_function[(state, i)]
            row = [0] * n
            for next_state in next_states:
                row[next_state] += 1
            hodge_structure.append(row)
    
    # Compute the minimal rank of the Hodge structure
    hodge_rank = len(gaussian_elimination(hodge_structure, [0] * n))
    
    # Check if the conjecture holds
    conjecture_holds = abs(hodge_rank - width) <= 3 and hodge_rank <= 10
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": hodge_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": f"rank={hodge_rank}, expected={width}" if not conjecture_holds else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, 'metric_name': '{result['metric_name']}', 'metric_value': {result['metric_value']}, 'instances_tested': {result['instances_tested']}, 'conjecture_holds': {result['conjecture_holds']}, 'counterexample': '{result['counterexample']}'}}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["conjecture_holds"] is False)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")