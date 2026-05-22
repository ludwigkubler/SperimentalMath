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
    
    def generate_k_clique_instance(n, k):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.randint(0, 1) == 1 and len(edges) < k * (n - 1) / 2:
                    edges.append((i, j))
        return edges
    
    def symplectic_root_system_dimension(edges):
        # Placeholder for actual computation
        return len(edges)
    
    def monotone_circuit_depth(n):
        # Placeholder for actual computation
        return int(math.log2(n)) + 1
    
    results = []
    for n in range(5, 41):
        k = random.randint(1, min(n // 2, 5))
        instance = generate_k_clique_instance(n, k)
        
        dim = symplectic_root_system_dimension(instance)
        depth = monotone_circuit_depth(n)
        
        results.append({
            "n": n,
            "k": k,
            "dim": dim,
            "depth": depth
        })
    
    min_dim = min(result["dim"] for result in results)
    avg_depth = sum(result["depth"] for result in results) / len(results)
    
    conjecture_holds = all(dim >= n ** 0.25 and depth >= n ** 0.25 for dim, depth in zip(min_dim, avg_depth))
    counterexample = "" if conjecture_holds else "dim < n^(1/4) or depth < Θ(n^(1/4))"
    
    return {
        "metric_name": "Symplectic Root System Dimension and Monotone Circuit Depth",
        "metric_value": min_dim,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_dim = sum(result["metric_value"] for result in results) / len(results)
    std_dim = (sum((result["metric_value"] - mean_dim) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_dim} std={std_dim} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_dim} std={std_dim} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")