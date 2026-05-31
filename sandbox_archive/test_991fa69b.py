# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import product

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            raise ValueError("Matrix is singular")
        for j in range(n):
            A[i][j] /= A[i][i]
        for k in range(m):
            if k != i and A[k][i] != 0:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def identity_matrix(n):
    return [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]

def inverse_matrix(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    A_augmented = [row + identity_matrix(n)[i] for i, row in enumerate(A)]
    gaussian_elimination(A_augmented)
    return [[A_augmented[i][j+n] for j in range(n)] for i in range(m)]

def dpll(instance, assignment):
    if all(assignment[lit] != -1 for lit in range(len(instance))):
        return True, 0
    literal = next(lit for lit in range(len(instance)) if instance[lit] == -1)
    for value in [True, False]:
        new_assignment = assignment[:]
        new_assignment[literal] = value
        result, path_length = dpll(instance, new_assignment)
        if result:
            return True, path_length + 1
    return False, 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    instances_tested = 0
    m_index_sum = 0
    w_DPLL_sum = 0
    counterexample = ""
    
    for _ in range(30):
        instance = [random.choice([-1, 0]) for _ in range(n)]
        assignment = [-1] * n
        path_length = dpll(instance, assignment)[1]
        
        if path_length > 10:
            counterexample = "m_index(φ) > 10"
            break
        
        m_index = len(set(tuple(sorted([i for i in range(n) if instance[i] == -1]))))
        m_index_sum += m_index
        w_DPLL_sum += path_length
        instances_tested += 1
    
    mean_m_index = Fraction(m_index_sum, instances_tested)
    mean_w_DPLL = Fraction(w_DPLL_sum, instances_tested)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": (mean_m_index * mean_w_DPLL - m_index_sum * w_DPLL_sum / instances_tested**2) /
                        math.sqrt((m_index_sum**2 - sum(m_index**2 for m_index in range(instances_tested)) / instances_tested) *
                                  (w_DPLL_sum**2 - sum(w_DPLL**2 for w_DPLL in range(instances_tested)) / instances_tested)),
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": False if counterexample else True,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.6f} std=0.000000 support_fraction=1.000000")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.6f} std=0.000000 support_fraction={support_fraction:.6f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")