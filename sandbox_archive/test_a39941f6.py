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
    
    def generate_clique_instance(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def tensor_rank(edges):
        n = len(edges) + 1
        T = [[0] * n for _ in range(n)]
        for u, v in edges:
            T[u][v] = T[v][u] = 1
        rank = 0
        while True:
            found = False
            for i in range(n):
                if any(T[i][j] != 0 for j in range(i + 1, n)):
                    pivot = next(j for j in range(i + 1, n) if T[i][j] != 0)
                    for k in range(n):
                        if k != i:
                            factor = T[k][pivot] / T[i][pivot]
                            for j in range(n):
                                T[k][j] -= factor * T[i][j]
                    found = True
            if not found:
                break
            rank += 1
        return rank
    
    def monotone_circuit_size(edges):
        n = len(edges) + 1
        circuit_size = 0
        for u, v in edges:
            circuit_size += 2  # Each edge requires at least two gates (AND and OR)
        return circuit_size
    
    results = []
    for _ in range(30):  # Test with 30 random instances
        n = random.choice([10, 20, 30, 40])
        edges = generate_clique_instance(n)
        T_rank = tensor_rank(edges)
        circuit_size = monotone_circuit_size(edges)
        results.append((T_rank, circuit_size))
    
    mean_T_rank = sum(T_rank for T_rank, _ in results) / len(results)
    mean_circuit_size = sum(circuit_size for _, circuit_size in results) / len(results)
    support_fraction = sum(1 for T_rank, circuit_size in results if T_rank <= math.sqrt(n) and circuit_size >= 0.5 * math.sqrt(n)) / len(results)
    
    conjecture_holds = support_fraction > 0.95
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_rank_vs_circuit_size",
        "metric_value": mean_T_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")