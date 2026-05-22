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
    
    n = random.randint(5, 40)
    G = {i: set() for i in range(n)}
    edges = random.sample(range(n * (n - 1)), random.randint(n * (n - 1) // 2, n * (n - 1)))
    for u, v in edges:
        if u != v and u not in G[v]:
            G[u].add(v)
            G[v].add(u)
    
    def tropical_curve(G):
        curve = {i: 0 for i in range(n)}
        for u in G:
            for v in G[u]:
                curve[u] = max(curve[u], curve[v] + 1)
        return curve
    
    curve = tropical_curve(G)
    fluctuation = sum(abs(curve[i] - curve[j]) for i in range(n) for j in range(i+1, n)) / (n * (n - 1) // 2)
    
    def monotone_circuit_size(k):
        return k**4
    
    k = random.randint(1, n)
    circuit_size = monotone_circuit_size(k)
    
    return {
        "metric_name": "geometric_fluctuation",
        "metric_value": fluctuation,
        "instances_tested": 1,
        "conjecture_holds": fluctuation >= math.sqrt(n),
        "counterexample": f"Graph with n={n}, fluctuation={fluctuation}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_fluctuation = sum(r["metric_value"] for r in results) / len(results)
    std_fluctuation = math.sqrt(sum((r["metric_value"] - mean_fluctuation) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_fluctuation} std={std_fluctuation} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Graph with n={seeds[0]}, fluctuation={results[0]['metric_value']}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")