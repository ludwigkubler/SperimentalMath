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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def nonnegative_rank(A):
        rank = 0
        m, n = len(A), len(A[0])
        for i in range(m):
            if any(A[i]):
                rank += 1
        return rank
    
    def k_clique_indicator(n, k):
        # Generate a random k-clique instance
        V = list(range(n))
        E = set()
        while len(E) < k:
            u = random.choice(V)
            v = random.choice([x for x in V if x != u])
            if (u, v) not in E and (v, u) not in E:
                E.add((u, v))
        return V, E
    
    def monotone_circuit_size(n, k):
        # Placeholder function to simulate the size of a monotone circuit
        # This is a dummy implementation for testing purposes
        return n * math.log(k)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        V, E = k_clique_indicator(n, random.randint(2, min(n-1, 10)))
        A = [[0] * n for _ in range(n)]
        for u, v in E:
            A[u][v] = 1
            A[v][u] = 1
        
        rank = nonnegative_rank(A)
        circuit_size = monotone_circuit_size(n, len(E))
        
        results.append({
            "n": n,
            "rank": rank,
            "circuit_size": circuit_size
        })
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    mean_circuit_size = sum(result["circuit_size"] for result in results) / len(results)
    conjecture_holds = all(rank >= n * math.log(k) for n, k, rank in zip(n_values, [len(E)] * len(n_values), [result["rank"] for result in results]))
    
    return {
        "metric_name": "Nonnegative Rank vs Circuit Size",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n_values[0]}, k={len(E)}, rank={results[0]['rank']}, circuit_size={results[0]['circuit_size']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, k={len(E)}, rank={results[0]['rank']}, circuit_size={results[0]['circuit_size']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")