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
    
    def generate_graph(n):
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    G[i][j] = G[j][i] = 1
        return G
    
    def tautology_degree(G):
        n = len(G)
        max_degree = 0
        
        for s in range(2**n):
            degree = 0
            for j in range(n):
                if (s >> j) & 1:
                    for k in range(j + 1, n):
                        if G[j][k] and (s >> k) & 1:
                            degree += 1
            max_degree = max(max_degree, degree)
        
        return max_degree
    
    def minimal_rank(G):
        n = len(G)
        I = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
        
        # Gaussian elimination to find the rank
        for i in range(n):
            if G[i][i] == 0:
                found = False
                for k in range(i + 1, n):
                    if G[k][i] != 0:
                        G[i], G[k] = G[k], G[i]
                        I[i], I[k] = I[k], I[i]
                        found = True
                        break
                if not found:
                    return i
        
            for j in range(n):
                if j == i:
                    continue
                factor = -G[j][i] / G[i][i]
                for k in range(n):
                    G[j][k] += factor * G[i][k]
                    I[j][k] += factor * I[i][k]
        
        return n
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = generate_graph(n)
    
    rank = minimal_rank(G)
    degree = tautology_degree(G)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= degree,
        "counterexample": "" if rank <= degree else f"Graph with n={n}, rank={rank}, degree={degree}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds = all(r["conjecture_holds"] for r in results)
    
    if conjecture_holds:
        mean = sum(metric_values) / len(metric_values)
        std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
        support_fraction = len(results) / len(seeds)
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")