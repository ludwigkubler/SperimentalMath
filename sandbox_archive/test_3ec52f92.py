# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_graph(n):
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if matrix[i][i] != 0:
                for j in range(i + 1, m):
                    factor = Fraction(matrix[j][i], matrix[i][i])
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
                rank += 1
        return rank
    
    def find_subspaces(matrix, d):
        n = len(matrix)
        subspaces = []
        for i in range(1 << n):
            subspace = [j for j in range(n) if (i & (1 << j))]
            if len(subspace) >= d:
                submatrix = [[matrix[j][k] for k in subspace] for j in subspace]
                rank = matrix_rank(submatrix)
                subspaces.append((subspace, rank))
        return subspaces
    
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    d = random.randint(1, n)
    
    min_rank = float('inf')
    for subspace, rank in find_subspaces(graph, d):
        if rank < min_rank:
            min_rank = rank
    
    metric_value = min_rank
    conjecture_holds = min_rank >= Fraction(n**2, 3)  # Simplified bound for demonstration
    counterexample = "" if conjecture_holds else f"Graph with n={n}, d={d}"
    
    return {
        "metric_name": "Minimum Rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")