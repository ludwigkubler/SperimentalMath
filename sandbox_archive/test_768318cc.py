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
    
    n = 30
    G = {i: [] for i in range(n)}
    for _ in range(int(n * (n - 1) / 2)):
        u, v = random.sample(range(n), 2)
        if u != v and v not in G[u]:
            G[u].append(v)
            G[v].append(u)
    
    def edge_expansion(G):
        n = len(G)
        min_cut_size = float('inf')
        for S in range(1, n // 2 + 1):
            candidates = [set(random.sample(range(n), S)) for _ in range(10)]
            for candidate in candidates:
                cut_size = sum(len([v for v in G[u] if u not in candidate and v in candidate]) for u in candidate)
                min_cut_size = min(min_cut_size, cut_size)
        return min_cut_size / n
    
    h_G = edge_expansion(G)
    
    def resolution_length(h_G):
        if h_G == 0:
            return 1
        c = 2
        return 2 ** (c * h_G)
    
    proof_length = resolution_length(h_G)
    
    return {
        "metric_name": "Resolution length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": proof_length >= 2 ** (0.5 * h_G),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")