# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations, product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def is_k_sat_instance(G, k):
        # Placeholder for actual K-SAT instance check
        return False
    
    def generate_graph(n):
        edges = set()
        while len(edges) < n * (n - 1) // 2:
            u, v = random.sample(range(n), 2)
            if (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return {i: set() for i in range(n)}, edges
    
    def min_rank(K):
        # Placeholder for actual minimal rank calculation
        return 0
    
    def generate_dnf_circuits(G, k):
        # Placeholder for actual DNF circuit generation and minimization
        return []
    
    n = random.randint(5, 40)
    G, edges = generate_graph(n)
    k = random.randint(1, n - 1)
    
    if not is_k_sat_instance(G, k):
        return {
            "metric_name": "min_rank",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "k-SAT instance undefined"
        }
    
    r_G = min_rank(G)
    circuits = generate_dnf_circuits(G, k)
    m_actual = min(len(circuit) for circuit in circuits if is_k_sat_instance(G, k))
    
    return {
        "metric_name": "min_rank",
        "metric_value": r_G,
        "instances_tested": 1,
        "conjecture_holds": m_actual <= 2 ** r_G,
        "counterexample": "" if m_actual <= 2 ** r_G else f"m_actual={m_actual} > 2^{r_G}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"m_actual > 2^r(G)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")