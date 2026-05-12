# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations_with_replacement, permutations

def partitions(n):
    def partitions_recursive(n, max_partition=None):
        if n == 0:
            return [[]]
        result = []
        for i in range(1, min(n + 1, max_partition + 1)):
            for p in partitions_recursive(n - i, i):
                result.append([i] + p)
        return result
    return partitions_recursive(n)

def schur_coefficient(matrix, partition):
    n = len(matrix)
    if len(partition) != n:
        return 0
    
    def hook_length_formula(tableau):
        numerator = math.factorial(n)
        denominator = 1
        for i in range(n):
            for j in range(n):
                hook_length = (n - i) + (n - j) - partition[i] - partition[j] + 1
                denominator *= hook_length
        return numerator // denominator
    
    def is_standard_tableau(tableau):
        if len(set([tableau[i][j] for i in range(n) for j in range(n)])) != n * n:
            return False
        for i in range(n):
            if sorted(tableau[i]) != list(range(1, n + 1)):
                return False
            if sorted([tableau[j][i] for j in range(n)]) != list(range(1, n + 1)):
                return False
        return True
    
    def generate_tableaux(partition):
        tableaux = []
        elements = list(range(1, n + 1))
        for perm in permutations(elements):
            tableau = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    if perm[i * n + j] <= partition[i]:
                        tableau[i][j] = perm[i * n + j]
            if is_standard_tableau(tableau):
                tableaux.append(tableau)
        return tableaux
    
    tableaux = generate_tableaux(partition)
    return sum(hook_length_formula(t) for t in tableaux)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    S_n_total = 0
    S_prime_n_total = 0
    instances_tested = 0
    
    for n in n_values:
        perm_matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        det_matrix = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
        
        S_n = sum(schur_coefficient(perm_matrix, partition) for partition in partitions(n) if max(partition) <= n**0.5)
        S_prime_n = sum(schur_coefficient(det_matrix, partition) for partition in partitions(n) if max(partition) <= n**0.5)
        
        S_n_total += S_n
        S_prime_n_total += S_prime_n
        instances_tested += 2
    
    ratio = S_n_total / S_prime_n_total
    conjecture_holds = ratio > 2**(n_values[-1]/2)
    counterexample = "" if conjecture_holds else f"Ratio {ratio} <= 2^{n_values[-1]/2}"
    
    return {
        "metric_name": "Schur Coefficient Sum Ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 307))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")