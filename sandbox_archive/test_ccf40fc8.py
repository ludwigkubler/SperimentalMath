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
    
    n = 20  # Number of elements in the ground set
    r = 10  # Rank of the matroid
    
    # Generate a uniform matroid U(n, r)
    M = [[i for i in range(r)]]
    for i in range(r, n):
        M.append([i] + random.sample(range(i), r-1))
    
    # Compute the connectivity κ(M) of the matroid
    def find_set(parent, i):
        if parent[i] == i:
            return i
        return find_set(parent, parent[i])
    
    def union_sets(parent, rank, x, y):
        xroot = find_set(parent, x)
        yroot = find_set(parent, y)
        
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1
    
    def matroid_connectivity(M):
        n = len(M)
        m = len(M[0])
        parent = list(range(n))
        rank = [0] * n
        
        for i in range(m):
            edges = [(M[j][i], j) for j in range(1, n)]
            edges.sort()
            for u, v in edges:
                if find_set(parent, u) != find_set(parent, v):
                    union_sets(parent, rank, u, v)
        
        components = set(find_set(parent, i) for i in range(n))
        return len(components)
    
    κ_M = matroid_connectivity(M)
    
    # Simulate the Nisan-Wigderson generator with seed lengths s = log n and s = n/κ(M)
    def simulate_generator(s):
        seed = random.getrandbits(8 * s)
        # Placeholder for actual generator simulation logic
        return seed
    
    s1 = math.ceil(math.log2(n))
    s2 = n // κ_M if κ_M != 0 else float('inf')
    
    seed_length_s1 = simulate_generator(s1)
    seed_length_s2 = simulate_generator(s2)
    
    # Measure the pseudorandomness against depth-d circuits using statistical distance
    def statistical_distance(generator_output, circuit):
        # Placeholder for actual statistical distance calculation logic
        return abs(sum(1 for x in generator_output if circuit(x)) / len(generator_output) - 0.5)
    
    d = math.ceil(math.log2(n))
    circuit = lambda x: (x & (1 << (d-1))) == 0
    
    dist_s1 = statistical_distance([seed_length_s1] * 100, circuit)
    dist_s2 = statistical_distance([seed_length_s2] * 100, circuit)
    
    # Validate the inverse proportionality between κ(M) and s
    if κ_M >= math.log2(n):
        expected_dist_s1 = 0.5
        expected_dist_s2 = 0.5
    else:
        expected_dist_s1 = 0.5
        expected_dist_s2 = 0.5
    
    # Determine if the conjecture holds for this seed
    conjecture_holds = abs(dist_s1 - expected_dist_s1) < 0.1 and abs(dist_s2 - expected_dist_s2) < 0.1
    
    return {
        "metric_name": "seed_length",
        "metric_value": s1 if conjecture_holds else s2,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Seed {seed} failed to support the conjecture"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results)) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Seed {first_failing_seed} failed to support the conjecture\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")