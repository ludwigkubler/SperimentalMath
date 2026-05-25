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
        n = len(A)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, n):
                factor = -A[j][i] / A[i][i]
                for k in range(i, n + 1):
                    A[j][k] += factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def tropicalize(A):
        n = len(A)
        T = [[-math.inf] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                T[i][j] = max(A[i][k] + A[k][j] for k in range(n))
        return T
    
    def communication_protocol(G, k):
        n = len(G)
        if k > n:
            return 0
        bits = 0
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j] == 1:
                    bits += math.ceil(math.log2(k))
        return bits
    
    def generate_random_graph(n):
        G = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            G[i][i] = 0
        return G
    
    n_values = [10, 15, 20, 25, 30]
    results = []
    
    for n in n_values:
        for _ in range(6):  # Ensure at least 30 instances per seed
            G = generate_random_graph(n)
            K = G  # Simplified K-group for demonstration
            tau_K = gaussian_elimination(K)
            bits = communication_protocol(G, k=3)  # Example value for k
            
            results.append({
                "metric_name": "communication_bits",
                "metric_value": bits,
                "instances_tested": 1,
                "conjecture_holds": bits >= tau_K,
                "counterexample": ""
            })
    
    mean_bits = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_bits": mean_bits,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_bits = sum(result["mean_bits"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.8) / len(results)
    
    if all(result["support_fraction"] >= 0.8 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_bits} std=NA support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")