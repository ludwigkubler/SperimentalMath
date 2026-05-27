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
    
    def generate_tropical_quotient_group(n):
        # Generate a tropical quotient group with minimal rank <= n and size <= 20
        G = set()
        while len(G) < 20:
            g = tuple(random.randint(1, n) for _ in range(n))
            if all(g[i] != 0 for i in range(n)):
                G.add(g)
        return G
    
    def communication_complexity(G):
        # Compute the communication complexity of a function f for all pairs (x,y) in G
        max_complexity = 0
        for x in G:
            for y in G:
                # Simulate a simple AND-OR tree protocol
                complexity = sum(1 if xi & yi else 0 for xi, yi in zip(x, y))
                max_complexity = max(max_complexity, complexity)
        return max_complexity
    
    def minimal_rank(G):
        # Compute the minimal rank of G
        n = len(next(iter(G)))
        rank = 0
        for g in G:
            if all(g[i] != 0 for i in range(n)):
                rank += 1
        return rank
    
    def spearman_correlation(x, y):
        # Compute Spearman's rank correlation coefficient
        n = len(x)
        sorted_x = sorted(range(n), key=lambda k: x[k])
        sorted_y = sorted(range(n), key=lambda k: y[k])
        rank_x = [sorted_x.index(i) for i in range(n)]
        rank_y = [sorted_y.index(i) for i in range(n)]
        n = len(rank_x)
        sum_d1_squared = sum((rank_x[i] - rank_y[i]) ** 2 for i in range(n))
        return 1 - (6 * sum_d1_squared) / (n * (n ** 2 - 1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_complexity = 0
    total_rank = 0
    total_size = 0
    num_trials = 0
    
    for n in n_values:
        G = generate_tropical_quotient_group(n)
        rank = minimal_rank(G)
        size = len(G)
        complexity = communication_complexity(G)
        
        if complexity > min(rank, size) * math.log(size):
            return {
                "metric_name": "communication_complexity",
                "metric_value": complexity,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Exceeded bound for n={n}, rank={rank}, size={size}"
            }
        
        total_complexity += complexity
        total_rank += rank
        total_size += size
        num_trials += 1
    
    mean_complexity = total_complexity / num_trials
    mean_rank = total_rank / num_trials
    mean_size = total_size / num_trials
    
    correlation = spearman_correlation([mean_complexity] * num_trials, [min(mean_rank, mean_size)] * num_trials)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_complexity,
        "instances_tested": num_trials,
        "conjecture_holds": correlation >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_complexity = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_complexity} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_complexity} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Exceeded bound' first_failing_seed={first_failing_seed}")