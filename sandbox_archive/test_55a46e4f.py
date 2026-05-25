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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_primes(k):
        primes = []
        num = 2
        while len(primes) < k:
            if is_prime(num):
                primes.append(num)
            num += 1
        return primes
    
    def generate_k_clique(n, k):
        if n < k:
            return None
        clique = set()
        for i in range(k):
            clique.add(i)
        for i in range(k, n):
            if random.choice(list(clique)) not in clique:
                clique.remove(random.choice(list(clique)))
                clique.add(i)
        return list(clique)
    
    def incidence_matrix(clique, n):
        matrix = [[0] * n for _ in range(n)]
        for node in clique:
            for other_node in clique:
                if node != other_node:
                    matrix[node][other_node] = 1
        return matrix
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for col in range(cols):
            pivot_row = -1
            for row in range(rank, rows):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row == -1:
                continue
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            for r in range(rows):
                if r != rank and matrix[r][col] != 0:
                    factor = matrix[r][col] / matrix[rank][col]
                    for c in range(cols):
                        matrix[r][c] -= factor * matrix[rank][c]
            rank += 1
        return rank
    
    def min_rank(matrix):
        return gaussian_elimination(matrix)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        clique = generate_k_clique(n, n - 1)
        if clique is None:
            continue
        matrix = incidence_matrix(clique, n)
        rank = min_rank(matrix)
        results.append({"n": n, "rank": rank})
    
    if not results:
        return {
            "metric_name": "min_rank",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_rank_values = [result["rank"] for result in results]
    if all(rank >= n - 1 for rank, n in zip(min_rank_values, n_values)):
        return {
            "metric_name": "min_rank",
            "metric_value": sum(min_rank_values) / len(min_rank_values),
            "instances_tested": len(results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        first_failing = next(i for i, (rank, n) in enumerate(zip(min_rank_values, n_values)) if rank < n - 1)
        return {
            "metric_name": "min_rank",
            "metric_value": sum(min_rank_values) / len(min_rank_values),
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"n={n_values[first_failing]} rank={min_rank_values[first_failing]}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        result = f"SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = results[next(i for i, result in enumerate(results) if not result["conjecture_holds"])["counterexample"]]
        result = f"FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)