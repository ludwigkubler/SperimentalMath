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
    
    def generate_boolean_algebra(n):
        B = {f"x{i}": i for i in range(n)}
        return B
    
    def dual_vector_space(B):
        V = [list(b.values()) for b in B.values()]
        return V
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def rank(A):
        rref = gaussian_elimination([row[:] for row in A])
        return sum(1 for row in rref if any(row))
    
    def read_twice_branching_program(size):
        P = [random.choice(['0', '1']) for _ in range(size)]
        return P
    
    def circuit_threshold(P):
        threshold = 0
        for i in range(len(P)):
            if P[i] == '1':
                threshold += 2 ** (len(P) - i - 1)
        return threshold
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_threshold = 0
    instances_tested = sum(n_values)
    
    for n in n_values:
        B = generate_boolean_algebra(n)
        V = dual_vector_space(B)
        rank_value = rank(V)
        total_rank += rank_value
        
        for _ in range(n):
            P = read_twice_branching_program(n)
            threshold_value = circuit_threshold(P)
            total_threshold += threshold_value
    
    mean_rank = total_rank / instances_tested
    mean_threshold = total_threshold / instances_tested
    ratio = mean_threshold / mean_rank if mean_rank != 0 else float('inf')
    
    conjecture_holds = abs(ratio - 1) <= 0.1
    counterexample = "" if conjecture_holds else f"Ratio {ratio} outside ±10% of 1"
    
    return {
        "metric_name": "Circuit Threshold / Rank Ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio outside ±10% of 1\" first_failing_seed={first_failing_seed}")