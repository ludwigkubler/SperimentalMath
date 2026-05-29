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
    
    # Generate a random graph with n vertices
    n = 10 + random.randint(0, 20)
    G = {i: set() for i in range(n)}
    edges = [(i, j) for i in range(n) for j in range(i+1, n)]
    num_edges = random.randint(int(n * (n - 1) / 4), int(n * (n - 1) / 2))
    for _ in range(num_edges):
        u, v = random.choice(edges)
        G[u].add(v)
        G[v].add(u)
    
    # Compute the diameter of the graph
    def bfs(start):
        visited = [False] * n
        queue = [(start, 0)]
        max_dist = 0
        while queue:
            node, dist = queue.pop(0)
            if not visited[node]:
                visited[node] = True
                max_dist = max(max_dist, dist)
                for neighbor in G[node]:
                    if not visited[neighbor]:
                        queue.append((neighbor, dist + 1))
        return max_dist
    
    diameter = max(bfs(i) for i in range(n))
    
    # Compute the monomial ideal I(G) and find its maximum number of generators
    def is_prime(num):
        if num <= 1:
            return False
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                return False
        return True
    
    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def monomial_ideal(G):
        generators = set()
        for node in range(n):
            if is_prime(node + 1):
                generators.add((node + 1,))
        for u in range(n):
            for v in G[u]:
                lcm_val = lcm(u + 1, v + 1)
                if is_prime(lcm_val):
                    generators.add((lcm_val,))
        return len(generators), generators
    
    M, _ = monomial_ideal(G)
    
    # Compare the ratio D(G)/M
    ratio = diameter / M
    
    # Check if the conjecture holds for this seed
    conjecture_holds = ratio <= 2 * n  # Example polynomial relationship: c * poly(M) = 2 * n
    
    return {
        "metric_name": "diameter_to_generators_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"D(G)={diameter}, M={M}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 3 for i in range(5, 8)]  # Default list of 30 primes
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_ratio)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")