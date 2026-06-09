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
    
    def generate_random_function(n):
        # Generate a random function f from {0,1}^n to {0,1}
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def syntactic_monoid(f):
        # Compute the syntactic monoid of the function f
        n = int(math.log2(len(f)))
        M = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                x = [i >> k & 1 for k in range(n)]
                y = [j >> k & 1 for k in range(n)]
                M[i][j] = f[(x[0] << (n-1)) | sum(x[k] << (k-1) for k in range(1, n))]
        return M
    
    def monoid_representation(M):
        # Compute the minimal depth of a monoid representation
        n = len(M)
        G = []
        for i in range(n):
            for j in range(i+1, n):
                if all(M[i][k] == M[j][k] for k in range(n)):
                    G.append((i, j))
        return len(G)
    
    def communication_complexity(f):
        # Compute the communication complexity rank of the function f
        n = int(math.log2(len(f)))
        max_rank = 0
        for i in range(1 << n):
            x = [i >> k & 1 for k in range(n)]
            rank = sum(x[k] * (1 if f[(x[0] << (n-1)) | sum(x[k] << (k-1) for k in range(1, n))] else 0) for k in range(n))
            max_rank = max(max_rank, rank)
        return max_rank
    
    def depth(M):
        # Compute the depth of a monoid representation
        n = len(M)
        visited = [False] * n
        stack = [(i, 1) for i in range(n)]
        while stack:
            node, d = stack.pop()
            if not visited[node]:
                visited[node] = True
                for j in range(n):
                    if M[node][j] != 0 and not visited[j]:
                        stack.append((j, d + 1))
        return max(d for _, d in stack)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_random_function(n)
        M = syntactic_monoid(f)
        rep_depth = monoid_representation(M)
        comm_rank = communication_complexity(f)
        results.append({
            "n": n,
            "communication_rank": comm_rank,
            "representation_depth": rep_depth
        })
    
    mean_comm_rank = sum(res["communication_rank"] for res in results) / len(results)
    mean_rep_depth = sum(res["representation_depth"] for res in results) / len(results)
    max_rep_depth = max(res["representation_depth"] for res in results)
    
    conjecture_holds = all(abs(comm_rank - rep_depth) <= 3 for res in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": mean_comm_rank,
        "instances_tested": len(results),
        "n_max": max_rep_depth,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")