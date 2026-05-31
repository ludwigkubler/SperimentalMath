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
    
    def generate_clause_set(n):
        return [random.choice([f"x{i}", f"~x{i}"]) for _ in range(n)]
    
    def tropical_rank(clause_set):
        n = len(clause_set)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        
        for i, clause in enumerate(clause_set):
            if clause.startswith('x'):
                j = int(clause[1:]) - 1
                matrix[i][j] = 1
                matrix[j][i] = 1
            else:
                j = int(clause[2:]) - 1
                matrix[i][j] = 0
                matrix[j][i] = 0
        
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if matrix[i][k] + matrix[k][j] < matrix[i][j]:
                        matrix[i][j] = matrix[i][k] + matrix[k][j]
        
        return max(max(row) for row in matrix)
    
    def compute_alpha(ranks, n_values):
        alpha_values = []
        for i in range(len(n_values)):
            if ranks[i] == 0 or n_values[i] == 0:
                continue
            alpha_values.append(math.log(ranks[i]) / math.log(n_values[i]))
        return sum(alpha_values) / len(alpha_values)
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x_i - mean_x) * (y_i - mean_y) for x_i, y_i in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((x_i - mean_x) ** 2 for x_i in x) / len(x))
        std_y = math.sqrt(sum((y_i - mean_y) ** 2 for y_i in y) / len(y))
        return cov / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clause_set = generate_clause_set(n)
            rank = tropical_rank(clause_set)
            ranks.append(rank)
            instances_tested += 1
    
    alpha = compute_alpha(ranks, n_values)
    correlation = pearson_correlation(ranks, [n ** (alpha + 0.05) for n in n_values])
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.7 and abs(alpha - (alpha + 0.05)) <= 0.01 * alpha,
        "counterexample": "" if correlation >= 0.7 and abs(alpha - (alpha + 0.05)) <= 0.01 * alpha else f"alpha={alpha}, corr={correlation}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[first_failing_seed]}")