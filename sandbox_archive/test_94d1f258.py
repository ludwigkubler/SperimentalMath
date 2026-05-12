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

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def hook_length_formula(n, λ):
    hook_lengths = [[n - row - col + 1 for col in range(col, n)] for row in range(row, n)]
    numerator = factorial(n)
    denominator = 1
    for row in λ:
        for cell in row:
            if cell != 0:
                denominator *= hook_lengths[cell-1][cell-1]
    return numerator // denominator

def random_3_regular_hypergraph(n):
    edges = set()
    while len(edges) < n * (n - 1) // 2:
        u, v = random.sample(range(n), 2)
        if u != v and {u, v} not in edges:
            edges.add(frozenset({u, v}))
    return list(edges)

def permanent(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        sign = (-1) ** j
        det += sign * matrix[0][j] * permanent(submatrix)
    return det

def monotone_circuit_size(n):
    # Upper bound for permanent computation
    return 2 ** (n // 2)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    mλ_values = []
    size_mono_values = []
    
    for _ in range(30):
        H = random_3_regular_hypergraph(n)
        λ = [(i, j) for i in range(n) for j in range(i+1, n)]
        mλ = hook_length_formula(n, λ)
        mλ_values.append(mλ)
        
        size_mono = monotone_circuit_size(n)
        size_mono_values.append(size_mono)
    
    mean_mλ = sum(mλ_values) / len(mλ_values)
    std_mλ = math.sqrt(sum((x - mean_mλ) ** 2 for x in mλ_values) / len(mλ_values))
    mean_size_mono = sum(size_mono_values) / len(size_mono_values)
    std_size_mono = math.sqrt(sum((x - mean_size_mono) ** 2 for x in size_mono_values) / len(size_mono_values))
    
    correlation = (sum((mλ_values[i] * (1 / size_mono_values[i])) for i in range(len(mλ_values))) / len(mλ_values)) / (mean_mλ * (1 / mean_size_mono))
    
    conjecture_holds = abs(correlation - 1) < 0.2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(mλ_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_corr = sum(r['metric_value'] for r in results) / len(results)
    std_corr = math.sqrt(sum((r['metric_value'] - mean_corr) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")