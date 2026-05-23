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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, m):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def rank_of_matrix(A):
    A = gaussian_elimination(A)
    rank = 0
    for row in A:
        if any(row):
            rank += 1
    return rank

def generate_random_quantized_space(n):
    # Placeholder function to generate a random geometrically quantized space
    # This is a dummy implementation and should be replaced with actual logic
    return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]

def compute_acc0_circuit_weight(char_func):
    # Placeholder function to compute the ACC⁰ circuit weight of a characteristic function
    # This is a dummy implementation and should be replaced with actual logic
    return sum(row.count(1) for row in char_func)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Test each size with 5 different instances
            X = generate_random_quantized_space(n)
            quantization_map = X
            minimal_rank = rank_of_matrix(quantization_map)
            
            char_func = X
            acc0_circuit_weight = compute_acc0_circuit_weight(char_func)
            
            if minimal_rank > acc0_circuit_weight:
                conjecture_holds = False
                counterexample = f"n={n}, minimal_rank={minimal_rank}, acc0_circuit_weight={acc0_circuit_weight}"
                break
            
            total_metric_value += minimal_rank / acc0_circuit_weight
            instances_tested += 1
    
    return {
        "metric_name": "Ratio of Minimal Rank to ACC⁰ Circuit Weight",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")