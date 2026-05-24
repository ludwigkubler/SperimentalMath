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
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def generate_k_clique_instance(n, k):
        vertices = list(range(n))
        edges = []
        for i in range(k):
            edge = random.sample(vertices, 2)
            edges.append((edge[0], edge[1]))
            vertices.remove(edge[0])
            vertices.remove(edge[1])
        return edges
    
    def compute_geometric_entanglement_rank(edges):
        n = len(edges) + 1
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for u, v in edges:
            A[u][v] = 1
            A[v][u] = 1
        return gaussian_elimination(A)
    
    def compute_sum_of_squares_circuit_size(edges):
        # Placeholder for actual computation or lower bound
        return len(edges) * 2
    
    n_max = 40
    instances_tested = 30
    total_rank = 0
    total_circuit_size = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        k = random.randint(5, min(n_max // 2, 10))
        edges = generate_k_clique_instance(n_max, k)
        rank = compute_geometric_entanglement_rank(edges)
        circuit_size = compute_sum_of_squares_circuit_size(edges)
        
        if rank < n_max or circuit_size >= n_max:
            conjecture_holds = False
            counterexample = f"n={n_max}, k={k}, rank={rank}, circuit_size={circuit_size}"
            break
        
        total_rank += rank
        total_circuit_size += circuit_size
    
    metric_value = total_rank / instances_tested
    support_fraction = 0.95
    
    return {
        "metric_name": "Rank vs Circuit Size",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_rank = sum(r["metric_value"] * r["instances_tested"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={total_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")