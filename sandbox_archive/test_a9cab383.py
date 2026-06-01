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

def generate_k_regular_graph(n, k):
    if (n * k) % 2 != 0:
        return None
    adj_matrix = [[0] * n for _ in range(n)]
    degree = k // 2
    nodes = list(range(n))
    random.shuffle(nodes)
    
    for i in range(n):
        neighbors = random.sample(nodes[:i] + nodes[i+1:], degree)
        for neighbor in neighbors:
            adj_matrix[i][neighbor] = 1
            adj_matrix[neighbor][i] = 1
    
    return adj_matrix

def gaussian_elimination(matrix, n):
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate non-pivot elements
        pivot = matrix[i][i]
        for j in range(n):
            if j != i:
                factor = Fraction(matrix[j][i], pivot)
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
    
    return matrix

def calculate_char_poly(adj_matrix, n):
    x = 1
    char_poly = [1]
    for row in adj_matrix:
        new_poly = []
        for i in range(len(char_poly)):
            new_poly.append(x * char_poly[i] - sum(row[j] * char_poly[j] for j in range(i)))
        char_poly = new_poly
    
    return char_poly

def calculate_mfr(G, k):
    n = len(G)
    adj_matrix = G
    char_poly = calculate_char_poly(adj_matrix, n)
    
    # Calculate the minimal rank of the modular form
    mfr_G = 0
    for coeff in char_poly:
        if coeff != 0:
            mfr_G += 1
    
    return mfr_G

def run_trial(seed: int) -> dict:
    random.seed(seed)
    k_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in k_values:
        G = generate_k_regular_graph(n, n-1)
        if G is None:
            continue
        
        mfr_G = calculate_mfr(G, n-1)
        expected_value = Fraction(n**((n-1)/2))
        
        results.append({
            "metric_name": "mfr/G",
            "metric_value": Fraction(mfr_G, n),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": abs(Fraction(mfr_G, n) - expected_value) <= Fraction(expected_value * 0.2),
            "counterexample": ""
        })
    
    return {
        "seed": seed,
        "metric_name": "mfr/G",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(result["n_max"] for result in results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mfr(G)/|G| exceeds ±20%\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")