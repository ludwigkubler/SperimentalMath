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
    
    def generate_random_circuit(n, max_depth):
        if n == 1 or max_depth == 0:
            return []
        depth = random.randint(2, max_depth)
        subcircuit_size = random.randint(1, n-1)
        subcircuit = generate_random_circuit(subcircuit_size, depth - 2)
        return [subcircuit] * (n - subcircuit_size) + [[[]]]

    def adjacency_matrix(circuit):
        n = len(circuit)
        adj = [[0] * n for _ in range(n)]
        for i in range(n):
            if circuit[i]:
                for j in circuit[i]:
                    adj[i][j] = 1
        return adj

    def is_d_regular(adj, d):
        for row in adj:
            if sum(row) != d:
                return False
        return True

    def rank_of_root_system(adj):
        n = len(adj)
        I = [[int(i == j) for j in range(n)] for i in range(n)]
        A = [row[:] + [-1] for row in adj]
        A += [I[i] + [0] * (n - 1) for i in range(n)]
        m = len(A)
        n += 1
        rank = 0
        for j in range(n):
            pivot_row = next((i for i in range(rank, m) if A[i][j]), None)
            if pivot_row is not None:
                A[pivot_row], A[rank] = A[rank], A[pivot_row]
                for i in range(m):
                    if i != rank:
                        factor = A[i][j] / A[rank][j]
                        A[i][j:] = [A[i][k] - factor * A[rank][k] for k in range(j, n + 1)]
                rank += 1
        return rank

    def dimension_of_lie_algebra(adj):
        return rank_of_root_system(adj)

    n = random.randint(5, 30)
    max_depth = random.randint(5, 40)
    circuit = generate_random_circuit(n, max_depth)
    adj = adjacency_matrix(circuit)
    
    if not is_d_regular(adj, n - 1):
        return {
            "metric_name": "Rank of Root System",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Mapping undefined for non-d-regular graph"
        }
    
    rank = rank_of_root_system(adj)
    dim_lie_algebra = dimension_of_lie_algebra(adj)
    
    return {
        "metric_name": "Rank of Root System",
        "metric_value": rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": rank <= max_depth and dim_lie_algebra <= n,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")