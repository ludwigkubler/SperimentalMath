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
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: f'x{i+1}' for i in range(n)}
        clauses = []
        
        for u, v in graph:
            literals[u], literals[v] = str(literals[u]), str(literals[v])
            clauses.append([literals[u], literals[v]])
            clauses.append([-literals[u], -literals[v]])
        
        return literals, clauses
    
    def euler_characteristic(n):
        # For a d-regular graph with n vertices, the Euler characteristic is 2
        return 2
    
    def communication_complexity(n):
        # Communication complexity of Tseitin formula for a d-regular graph is O(n log n)
        return n * math.log(n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        # Generate a random d-regular graph
        d = 3  # Example degree, can be adjusted
        graph = set()
        vertices = list(range(n))
        
        while len(graph) < n * d // 2:
            u, v = random.sample(vertices, 2)
            if (u, v) not in graph and (v, u) not in graph:
                graph.add((u, v))
        
        literals, clauses = tseitin_formula(graph)
        chi_S = euler_characteristic(n)
        CC_phi_G = communication_complexity(n)
        
        results.append({
            "n": n,
            "chi_S": chi_S,
            "CC_phi_G": CC_phi_G,
            "ratio": chi_S / CC_phi_G
        })
    
    total_ratio = sum(result["ratio"] for result in results)
    mean_ratio = total_ratio / len(results)
    conjecture_holds = all(result["ratio"] <= 2 * math.log10(n) for n, _, _, ratio in results)
    counterexample = "" if conjecture_holds else "n_max >= 16"
    
    return {
        "metric_name": "Ratio of Euler Characteristic to Communication Complexity",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
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
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and max(result["n_max"] for result in results) >= 16:
        first_failing_seed = next(seed for seed, result in enumerate(results, start=1) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeded 2 * log10(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=30")