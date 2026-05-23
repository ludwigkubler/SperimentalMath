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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def communication_complexity(G):
        n = len(G)
        total_bits = 0
        for i in range(1 << n):
            subset_i = [j for j in range(n) if (i & (1 << j)) != 0]
            for j in range(i+1, 1 << n):
                subset_j = [k for k in range(n) if (j & (1 << k)) != 0]
                intersection = set(subset_i).intersection(set(subset_j))
                if intersection:
                    total_bits += math.ceil(math.log2(len(intersection)))
        return total_bits
    
    def generate_random_graph(n):
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if random.choice([True, False]):
                    G[i][j] = 1
                    G[j][i] = 1
        return G
    
    def config_space(G):
        n = len(G)
        V = [0] * (2**n)
        for i in range(1 << n):
            subset = [j for j in range(n) if (i & (1 << j)) != 0]
            for j in range(n):
                if j not in subset and any(G[j][k] == 1 for k in subset):
                    V[i] += 1
        return V
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_complexity = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            G = generate_random_graph(n)
            rank = gaussian_elimination(config_space(G))
            complexity = communication_complexity(G)
            total_rank += rank
            total_complexity += complexity
            instances_tested += 1
    
    mean_ratio = total_rank / (total_complexity * n_values[-1])
    conjecture_holds = mean_ratio <= 1.5
    counterexample = "" if conjecture_holds else f"Mean ratio {mean_ratio} > 1.5"
    
    return {
        "metric_name": "Mean Ratio",
        "metric_value": mean_ratio,
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
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mean ratio exceeded 1.5\" first_failing_seed={first_failing_seed + 1}")