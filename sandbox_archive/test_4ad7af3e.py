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
    
    def generate_graph(n):
        edges = set()
        for _ in range(int(n * (n - 1) / 2)):
            u, v = random.sample(range(n), 2)
            if u < v and (u, v) not in edges:
                edges.add((u, v))
        return {u: [] for u in range(n)}, edges
    
    def compute_tropical_curve(graph):
        V, E = graph
        n = len(V)
        curve = [0] * n
        for u, v in E:
            curve[u] += 1
            curve[v] += 1
        return curve
    
    def geometric_fluctuation(curve):
        max_val = max(curve)
        min_val = min(curve)
        if max_val == min_val:
            return 0
        return (max_val - min_val) / (max_val + min_val)
    
    n = random.randint(5, 40)
    graph = generate_graph(n)
    curve = compute_tropical_curve(graph)
    fluctuation = geometric_fluctuation(curve)
    
    return {
        "metric_name": "geometric_fluctuation",
        "metric_value": fluctuation,
        "instances_tested": 1,
        "conjecture_holds": fluctuation >= math.sqrt(n),
        "counterexample": f"Graph with n={n}, fluctuation={fluctuation}" if fluctuation < math.sqrt(n) else ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        print(f"RESULT: FALSIFIED counterexample=\"Graph with n=40, fluctuation={results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")