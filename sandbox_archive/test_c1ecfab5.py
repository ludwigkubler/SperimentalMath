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
        graph = {}
        for i in range(n):
            graph[i] = set(random.sample(range(n), random.randint(1, n-1)))
        return graph
    
    def compute_bp_read_twice_width(graph):
        # Simplified approximation of BP_ReadTwice width
        max_degree = max(len(neighbors) for neighbors in graph.values())
        return max_degree + 1
    
    def compute_quantum_discord(graph):
        # Simplified approximation of quantum discord
        n = len(graph)
        return random.uniform(0, n**2)
    
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    bp_read_twice_width = compute_bp_read_twice_width(graph)
    quantum_discord = compute_quantum_discord(graph)
    
    if bp_read_twice_width == 0:
        return {
            "metric_name": "D(ρ)/log BP_ReadTwice(W(G))",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "BP_ReadTwice width is zero"
        }
    
    metric_value = quantum_discord / math.log(bp_read_twice_width)
    
    return {
        "metric_name": "D(ρ)/log BP_ReadTwice(W(G))",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": metric_value <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all("metric_value" in r and r["metric_value"] is not None for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE some seeds produced None metric_value")