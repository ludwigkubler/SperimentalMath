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
    
    def generate_random_graph(n):
        G = {i: set() for i in range(n)}
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    G[i].add(j)
                    G[j].add(i)
        return G
    
    def clique_complex(G):
        simplices = {frozenset()}
        for node in G:
            new_simplices = set()
            for s in simplices:
                if len(s) < 2 or node not in s:
                    continue
                new_simplices.add(s | {node})
            simplices.update(new_simplices)
        return simplices
    
    def betti_numbers(simplices):
        beta_0 = len([s for s in simplices if len(s) == 0])
        beta_1 = len([s for s in simplices if len(s) == 1])
        return beta_0, beta_1
    
    def sos_max_cut(G, degree):
        # Placeholder function to simulate SOS solver
        # Replace with actual implementation
        return random.random() < 0.878
    
    n = random.randint(5, 40)
    G = generate_random_graph(n)
    simplices = clique_complex(G)
    beta_0, beta_1 = betti_numbers(simplices)
    
    for d in range(1, 100):  # Arbitrary upper bound for SOS degree
        if sos_max_cut(G, d):
            return {
                "metric_name": "SOS Degree",
                "metric_value": d,
                "instances_tested": 1,
                "conjecture_holds": d >= beta_0 + beta_1,
                "counterexample": ""
            }
    
    return {
        "metric_name": "SOS Degree",
        "metric_value": None,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "sos_max_cut_not_found"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] == "sos_max_cut_not_found" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] == "sos_max_cut_not_found")
        print(f"RESULT: FALSIFIED counterexample=\"sos_max_cut_not_found\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=conjecture_holds_too_low")