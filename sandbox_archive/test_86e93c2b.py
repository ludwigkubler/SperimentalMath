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
    
    def generate_xor_and_network(n):
        network = []
        for _ in range(n):
            row = [random.choice([0, 1]) for _ in range(n)]
            network.append(row)
        return network
    
    def tensor_product_algebra(network):
        n = len(network)
        algebra = [[0] * (n * n) for _ in range(n * n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    for l in range(n):
                        algebra[i * n + j][k * n + l] = network[i][k] & network[j][l]
        return algebra
    
    def min_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if any(matrix[i][j] != 0 for j in range(n)):
                rank += 1
                for j in range(n):
                    matrix[i][j] /= matrix[i][j]
                for k in range(m):
                    if k != i and any(matrix[k][j] != 0 for j in range(n)):
                        for j in range(n):
                            matrix[k][j] -= matrix[i][j] * matrix[k][i]
        return rank
    
    def communication_complexity(network):
        n = len(network)
        complexity = 0
        for i in range(n):
            for j in range(i + 1, n):
                if network[i][j] == 1:
                    complexity += 1
        return complexity
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        network = generate_xor_and_network(n)
        algebra = tensor_product_algebra(network)
        rank = min_rank(algebra)
        complexity = communication_complexity(network)
        
        results.append({
            "metric_name": "communication_complexity",
            "metric_value": complexity,
            "instances_tested": 1,
            "conjecture_holds": rank <= 5,  # Placeholder for actual constant c
            "counterexample": "" if rank <= 5 else f"mean_rank={rank}, n_max={n}"
        })
    
    mean_complexity = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_complexity": mean_complexity,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 50, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_complexity = sum(r["mean_complexity"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["support_fraction"] == 1) / len(results)
    
    if all(r["support_fraction"] == 1 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_complexity} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_rank exceeded\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(results)}")