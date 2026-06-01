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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    k = 3  # Example value for k-regular graph, can be adjusted
    n_max = 40
    instances_tested = 0
    ratios = []
    
    for _ in range(30):  # Aim for at least 30 instances per seed
        n = random.randint(5, n_max)
        G = generate_k_regular_graph(n, k)
        
        if not G:
            continue
        
        mfr_G = calculate_minimal_rank(G)
        ratio = Fraction(mfr_G, n).limit_denominator()
        ratios.append(ratio)
        
        instances_tested += 1
    
    mean_ratio = sum(r for r in ratios) / len(ratios)
    support_count = sum(1 for r in ratios if abs(r - mean_ratio) <= 0.1 * (n_max ** (k / 2)))
    
    conjecture_holds = support_count >= 0.8 * len(ratios)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mfr(G) / |G|",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def generate_k_regular_graph(n: int, k: int) -> list:
    if (n * k) % 2 != 0 or k > n - 1:
        return None
    
    adj_matrix = [[0] * n for _ in range(n)]
    
    def add_edge(u: int, v: int):
        adj_matrix[u][v] = 1
        adj_matrix[v][u] = 1
    
    for i in range(n):
        neighbors = random.sample(range(n), k)
        for neighbor in neighbors:
            if i != neighbor and adj_matrix[i][neighbor] == 0:
                add_edge(i, neighbor)
    
    return adj_matrix

def calculate_minimal_rank(G: list) -> int:
    n = len(G)
    A = G
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            
            if A[i][i] == 0:
                return None
            
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        
        rank = sum(1 for row in A if any(row))
        return rank
    
    rank = gaussian_elimination(A)
    return rank

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"] - (r["n_max"] ** (r["k"] / 2))) > 0.2 * (r["n_max"] ** (r["k"] / 2)) for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if abs(r["metric_value"] - (r["n_max"] ** (r["k"] / 2))) > 0.2 * (r["n_max"] ** (r["k"] / 2)))
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")