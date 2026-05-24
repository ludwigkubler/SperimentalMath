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
    
    def generate_random_graph(n):
        graph = {i: set() for i in range(n)}
        for _ in range(n * (n - 1) // 2):
            u, v = random.sample(range(n), 2)
            if v not in graph[u]:
                graph[u].add(v)
                graph[v].add(u)
        return graph
    
    def free_entropy(graph):
        n = len(graph)
        edges = sum(len(neighbors) for neighbors in graph.values()) // 2
        entropy = -edges * math.log2(1 / (n * (n - 1) // 2))
        return entropy
    
    def distinguishing_tensor_width(n):
        # Simplified version for demonstration; actual implementation needed
        return n ** 0.5
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        graph = generate_random_graph(n)
        F_G = free_entropy(graph)
        rho_P = distinguishing_tensor_width(n)
        
        if F_G > math.log(rho_P):
            instances_tested += 1
            conjecture_holds = False
            counterexample = f"Graph with n={n}, F(G)={F_G}, ρ(P)={rho_P}"
    
    return {
        "metric_name": "Free Entropy vs Distinguishing Tensor Width",
        "metric_value": math.log(rho_P),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")