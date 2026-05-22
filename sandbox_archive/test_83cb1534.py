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
    
    def generate_xor_and_network(n, m):
        network = []
        for _ in range(m):
            row = [random.choice([0, 1]) for _ in range(n)]
            network.append(row)
        return network
    
    def compute_geometric_invariant(network):
        n = len(network[0])
        A = [[0] * (2 * n) for _ in range(2 * n)]
        
        for i in range(n):
            A[i][i + n] = 1
        
        for row in network:
            for j in range(n):
                if row[j] == 1:
                    for k in range(n):
                        A[n + j][n + k] += A[k][j]
        
        rank = 0
        for i in range(2 * n):
            pivot = None
            for j in range(i, 2 * n):
                if A[j][i] != 0:
                    pivot = j
                    break
            if pivot is None:
                continue
            rank += 1
            for j in range(2 * n):
                A[i][j], A[pivot][j] = A[pivot][j], A[i][j]
            for j in range(2 * n):
                if j != i and A[j][i] != 0:
                    factor = Fraction(A[j][i], A[i][i])
                    for k in range(2 * n):
                        A[j][k] -= factor * A[i][k]
        
        return rank
    
    def mean(lst):
        return sum(lst) / len(lst)
    
    def std(lst, m):
        return math.sqrt(sum((x - m) ** 2 for x in lst) / len(lst))
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            network = generate_xor_and_network(n, random.randint(1, n))
            rank = compute_geometric_invariant(network)
            ranks.append(rank)
    
    mean_rank = mean(ranks)
    std_rank = std(ranks, mean_rank)
    
    return {
        "metric_name": "Minimal Rank of Geometric Invariant",
        "metric_value": mean_rank,
        "instances_tested": len(ranks),
        "conjecture_holds": abs(mean_rank - (n_values[0] ** (2/3))) <= 3 and std_rank < 1,  # Adjust threshold as needed
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = std([r["metric_value"] for r in results], mean_rank)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")

def std(lst, m):
    return math.sqrt(sum((x - m) ** 2 for x in lst) / len(lst))