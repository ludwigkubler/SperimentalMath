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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def random_quasigroup(n):
    q = [[0] * n for _ in range(n)]
    elements = list(range(n))
    random.shuffle(elements)
    for i in range(n):
        for j in range(n):
            q[i][j] = elements[(i + j) % n]
    return q

def min_index(q):
    n = len(q)
    count = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if q[i][j] == q[k][i]:
                    count[j][k] += 1
    return max(max(row) for row in count)

def communication_complexity_rank(matrix):
    n = len(matrix)
    adj_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 1:
                adj_matrix[i][j] = 1
                adj_matrix[j][i] = 1
    
    def dfs(v, visited):
        stack = [v]
        while stack:
            v = stack.pop()
            if not visited[v]:
                visited[v] = True
                for j in range(n):
                    if adj_matrix[v][j] == 1 and not visited[j]:
                        stack.append(j)
    
    visited = [False] * n
    components = 0
    for i in range(n):
        if not visited[i]:
            dfs(i, visited)
            components += 1
    
    return components - 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        q = random_quasigroup(n)
        min_idx = min_index(q)
        matrix = [[int(q[i][j] == k) for j in range(n)] for k in range(n)]
        rank = communication_complexity_rank(matrix)
        results.append((min_idx, rank))
    
    correlation_sum = 0
    instances_tested = len(results)
    n_max = max(n for _, _ in results)
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    for i in range(instances_tested):
        for j in range(i + 1, instances_tested):
            min_idx_i, rank_i = results[i]
            min_idx_j, rank_j = results[j]
            correlation_sum += (min_idx_i - min_idx_j) * (rank_i - rank_j)
    
    n_pairs = instances_tested * (instances_tested - 1) // 2
    mean_corr = correlation_sum / n_pairs
    
    return {
        "metric_name": "correlation",
        "metric_value": mean_corr,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(mean_corr) >= 0.8,
        "counterexample": "" if abs(mean_corr) >= 0.8 else "correlation below threshold"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] is not None for r in results):
        first_failing_seed = min(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation below threshold' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")