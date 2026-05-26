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
    
    def generate_matrix(n):
        return [[random.choice([-1, 0, 1]) for _ in range(n)] for _ in range(n)]
    
    def communication_complexity(M):
        n = len(M)
        support_size = sum(sum(row) for row in M)
        return support_size * (n - support_size)
    
    def min_rank_quadratic_form(M):
        n = len(M)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                A[i][j] = sum(M[x][y] * M[y][x] for x in range(n) for y in range(n))
        rank = 0
        for i in range(n):
            if all(A[j][i] == 0 for j in range(rank)):
                continue
            pivot_row = rank
            for j in range(rank, n):
                if A[j][i] != 0:
                    break
            A[pivot_row], A[j] = A[j], A[pivot_row]
            for j in range(n):
                if i == j:
                    A[i][j] /= A[i][i]
                else:
                    A[j][i] /= A[i][i]
                    for k in range(i, n):
                        A[j][k] -= A[i][k]
            rank += 1
        return rank
    
    def spearman_correlation(ranks1, ranks2):
        n = len(ranks1)
        if n != len(ranks2):
            raise ValueError("Ranks lists must be of the same length")
        
        sorted_ranks1 = sorted(range(n), key=lambda i: ranks1[i])
        sorted_ranks2 = sorted(range(n), key=lambda i: ranks2[i])
        
        rank_diffs_squared_sum = sum((sorted_ranks1[i] - sorted_ranks2[i]) ** 2 for i in range(n))
        rho_numerator = n * rank_diffs_squared_sum
        rho_denominator = (n * (n**2 - 1)) / 6
        
        return 1 - (6 * rho_numerator) / rho_denominator
    
    def is_prime(num):
        if num <= 1:
            return False
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                return False
        return True
    
    primes = [i for i in range(5, 100) if is_prime(i)]
    seeds = [random.choice(primes) for _ in range(30)] if not sys.argv[1:] else list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        random.seed(seed)
        n = random.randint(5, 40)
        M = generate_matrix(n)
        cc = communication_complexity(M)
        min_rank = min_rank_quadratic_form(M)
        
        if cc == 0 or min_rank == 0:
            continue
        
        ratios = [min_rank / (cc ** c) for c in range(1, 4)]
        results.append({
            "metric_name": "Spearman's rank correlation",
            "metric_value": spearman_correlation(ratios, ratios),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        })
    
    if not results:
        return {
            "seed": seed,
            "metric_name": "Spearman's rank correlation",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no_data"
        }
    
    mean_metric = sum(result["metric_value"] for result in results) / len(results)
    std_metric = math.sqrt(sum((result["metric_value"] - mean_metric) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "metric_name": "Spearman's rank correlation",
        "metric_value": mean_metric,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] if sys.argv[1:] else [random.choice([i for i in range(5, 100) if is_prime(i)]) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric = sum(result["metric_value"] for result in results) / len(results)
    std_metric = math.sqrt(sum((result["metric_value"] - mean_metric) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")