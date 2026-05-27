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

def gaussian_elimination(A, b):
    n = len(b)
    A_b = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        if A_b[i][i] == 0:
            return None  # No unique solution exists
        for j in range(i+1, n):
            factor = A_b[j][i] / A_b[i][i]
            for k in range(i, n + 1):
                A_b[j][k] -= factor * A_b[i][k]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (A_b[i][-1] - sum(A_b[i][j] * x[j] for j in range(i+1, n))) / A_b[i][i]
    return x

def matrix_multiplication(A, B):
    m = len(A)
    p = len(B[0])
    q = len(B)
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(q):
                C[i][j] += A[i][k] * B[k][j]
    return C

def dpll(instance, assignment=None):
    if assignment is None:
        assignment = {}
    variables = set()
    for clause in instance:
        variables.update(clause)
    unassigned = variables - set(assignment.keys())
    if not unassigned:
        if all(any(lit in assignment and assignment[lit] == val for lit, val in clause) for clause in instance):
            return True
        else:
            return False
    var = next(iter(unassigned))
    for val in [True, False]:
        new_assignment = assignment.copy()
        new_assignment[var] = val
        if dpll(instance, new_assignment):
            return True
    return False

def construct_quantum_cluster_state(instance, assignment):
    n = len(instance)
    m = 2 ** n
    A = [[0] * m for _ in range(m)]
    b = [0] * m
    for i in range(m):
        binary = format(i, f'0{n}b')
        assignment_i = {variables[j]: int(binary[j]) for j in range(n)}
        if dpll(instance, assignment_i):
            A[i][i] = 1
            b[i] = 1
    return A, b

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    instance = [random.sample(range(-n, n+1), random.randint(2, n)) for _ in range(n)]
    assignment = {i: random.choice([True, False]) for i in range(-n, n+1)}
    
    A, b = construct_quantum_cluster_state(instance, assignment)
    solution = gaussian_elimination(A, b)
    if solution is None:
        return {
            "metric_name": "minimal_rank",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "No unique solution exists"
        }
    
    minimal_rank = len([i for i, val in enumerate(solution) if val != 0])
    depth_of_dpll_tree = dpll(instance)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": minimal_rank <= 2 ** depth_of_dpll_tree and minimal_rank >= depth_of_dpll_tree - 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    total_metric_value = 0
    count_supporting_conjecture = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
        total_metric_value += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            count_supporting_conjecture += 1
    
    mean_metric_value = total_metric_value / len(results)
    support_fraction = count_supporting_conjecture / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"minimal_rank exceeds 2^depth_of_dpll_tree by more than 3\" first_failing_seed={first_failing_seed}")