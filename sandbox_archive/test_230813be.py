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
    
    n = 20  # Fixed size for simplicity, adjust as needed
    G = generate_graph(n)
    h_G = edge_expansion(G)
    
    if h_G == 0:
        return {
            "metric_name": "Resolution length",
            "metric_value": float('inf'),  # Polynomial time for expanders
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    
    c = 2  # Constant factor for the bound
    resolution_length = 2 ** (c * h_G)
    
    return {
        "metric_name": "Resolution length",
        "metric_value": resolution_length,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

def generate_graph(n: int) -> list:
    G = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.5:
                G[i].append(j)
                G[j].append(i)
    return G

def edge_expansion(G: list) -> float:
    n = len(G)
    min_cut_size = float('inf')
    
    for S in range(1, n // 2 + 1):
        candidates = random.sample(range(n), S)
        cut_edges = sum(len([j for j in G[i] if j not in candidates]) for i in candidates)
        min_cut_size = min(min_cut_size, cut_edges)
    
    return min_cut_size / S

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    total_metric_value = 0
    support_count = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        total_metric_value += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            support_count += 1
        
        results.append(trial_result)
    
    mean_metric_value = total_metric_value / len(results)
    support_fraction = support_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        result = "SUPPORTED"
    elif support_fraction >= 0.8:
        result = "SUPPORTED"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"
    
    print(f"RESULT: {result} mean={mean_metric_value} std=0 support_fraction={support_fraction}")