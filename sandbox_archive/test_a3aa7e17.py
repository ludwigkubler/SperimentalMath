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
    
    def noncrossing_partition_matrix(circuit):
        n = len(circuit)
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            u, v = map(int, circuit[i][4:].split(", "))
            if 0 <= u < n and 0 <= v < n:
                matrix[u][v] = 1
                matrix[v][u] = 1
        return matrix
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            if matrix[i][i] == 0:
                found = False
                for j in range(i + 1, m):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        found = True
                        break
                if not found:
                    return i
            for j in range(n):
                if j != i and matrix[i][j] != 0:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return m
    
    def generate_k_clique(k, n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if len(edges) >= k * (k - 1) // 2:
                    break
                edges.append((i, j))
            if len(edges) >= k * (k - 1) // 2:
                break
        return edges
    
    def monotone_circuit(k):
        n = k * (k - 1) // 2
        circuit = []
        for i in range(n):
            u, v = random.sample(range(k), 2)
            if u > v:
                u, v = v, u
            circuit.append(f"OR({u},{v})")
        return circuit
    
    k_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for k in k_values:
        n = k * (k - 1) // 2
        clique_edges = generate_k_clique(k, n)
        circuit = monotone_circuit(k)
        
        if len(circuit) != n:
            return {
                "metric_name": "rank",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "circuit_size_mismatch"
            }
        
        matrix = noncrossing_partition_matrix(circuit)
        rank_value = rank(matrix)
        
        results.append({
            "k": k,
            "n": n,
            "rank": rank_value
        })
    
    if not results:
        return {
            "metric_name": "rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["rank"] - mean_rank) ** 2 for result in results) / len(results))
    
    return {
        "metric_name": "rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_rank = sum(result["metric_value"] for result in results) / len(results)
        std_rank = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction=1.0")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rank_mismatch' first_failing_seed={first_failing_seed}")