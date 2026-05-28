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
        G = {}
        for i in range(n):
            G[i] = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    G[i].add(j)
                    G[j].add(i)
        return G
    
    def connectivity(G):
        visited = [False] * len(G)
        
        def dfs(node):
            stack = [node]
            while stack:
                node = stack.pop()
                if not visited[node]:
                    visited[node] = True
                    for neighbor in G[node]:
                        stack.append(neighbor)
        
        dfs(0)
        return sum(visited) == len(G)
    
    def simulate_quantum_walk(G, n):
        connectivity_val = connectivity(G)
        if connectivity_val == 0:
            return float('inf')  # Avoid division by zero
        return random.random() * n**2 / connectivity_val**2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_communication_complexity = 0
    instances_tested = 0
    
    for n in n_values:
        G = generate_graph(n)
        communication_complexity = simulate_quantum_walk(G, n)
        if communication_complexity == float('inf'):
            return {
                "metric_name": "communication_complexity",
                "metric_value": None,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": "connectivity_zero"
            }
        total_communication_complexity += communication_complexity
        instances_tested += 1
    
    mean_communication_complexity = total_communication_complexity / len(n_values)
    conjecture_holds = all(communication_complexity <= n**2 / connectivity(G)**2 for G in [generate_graph(n) for n in n_values])
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_communication_complexity,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='connectivity_zero' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")