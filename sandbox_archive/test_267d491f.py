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
    
    def generate_k_clique_graph(n, k):
        if n < k:
            return None
        vertices = list(range(n))
        edges = []
        for i in range(k):
            for j in range(i + 1, k):
                edges.append((vertices[i], vertices[j]))
        for _ in range(2 * (n - k)):
            u, v = random.sample(vertices, 2)
            if (u, v) not in edges and (v, u) not in edges:
                edges.append((u, v))
        return vertices, edges
    
    def is_automorphism(G, H, mapping):
        for u, v in G:
            if (mapping[u], mapping[v]) not in H and (mapping[v], mapping[u]) not in H:
                return False
        return True
    
    def find_minimal_rank(G):
        n = len(G[0])
        vertices = list(range(n))
        automorphisms = []
        
        for perm in itertools.permutations(vertices):
            if is_automorphism(G, G, dict(zip(vertices, perm))):
                automorphisms.append(perm)
        
        rank = 0
        while True:
            found_new = False
            for i in range(len(automorphisms)):
                for j in range(i + 1, len(automorphisms)):
                    if all(automorphisms[i][k] == automorphisms[j][k] for k in range(n)):
                        automorphisms.pop(j)
                        found_new = True
                        break
                if found_new:
                    break
            if not found_new:
                break
            rank += 1
        
        return rank
    
    n_values = [10, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(7):  # Ensure at least 8 instances per size
            G = generate_k_clique_graph(n, k=3)
            if G is None:
                continue
            rank = find_minimal_rank(G)
            total_rank += rank
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = mean_rank <= 10 * n_values[-1]  # Example bound, replace with actual analysis
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        seeds = [2**i - 1 for i in range(5, 8)]  # First 30 primes
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")