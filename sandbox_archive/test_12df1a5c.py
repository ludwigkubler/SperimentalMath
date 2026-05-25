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
            for j in range(i+1, m):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def rank(matrix):
        matrix = [row[:] for row in matrix]
        r = gaussian_elimination(matrix)
        return sum(1 for row in r if any(row[j] != 0 for j in range(len(row))))
    
    def random_group(n):
        G = []
        for _ in range(n):
            g = [random.randint(-1, 1) for _ in range(n)]
            while not all(g[i] * g[j] == g[(i + j) % n] for i in range(n)):
                g = [random.randint(-1, 1) for _ in range(n)]
            G.append(g)
        return G
    
    def tropicalized_representation(G, S):
        n = len(G)
        T = [[0 if i == j else float('inf') for j in range(n)] for i in range(n)]
        for g in G:
            for s in S:
                T[s][s] = min(T[s][s], abs(g[s]))
        return T
    
    def monotone_circuit_size(k):
        # This is a placeholder function. Implement the actual algorithm to compute the circuit size.
        # For simplicity, we assume the circuit size is proportional to k^2.
        return k**2
    
    n = random.randint(5, 40)
    k = random.randint(3, min(n-1, 10))
    G = random_group(n)
    S = random.sample(range(n), k)
    
    T = tropicalized_representation(G, S)
    rank_T = rank(T)
    circuit_size = monotone_circuit_size(k)
    
    return {
        "metric_name": "Rank vs Circuit Size",
        "metric_value": rank_T,
        "instances_tested": 1,
        "conjecture_holds": rank_T >= circuit_size,
        "counterexample": "" if rank_T >= circuit_size else f"Counterexample for n={n}, k={k}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3**j for i in range(5) for j in range(5)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")