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
        graph = [[] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    graph[i].append(j)
                    graph[j].append(i)
        return graph
    
    def local_indeterminacy(graph):
        n = len(graph)
        indeterminacy = n
        for i in range(n):
            neighbors = set(graph[i])
            for j in range(i + 1, n):
                if j not in neighbors:
                    indeterminacy -= 1
                    break
        return indeterminacy
    
    def circuit_monotone_width(graph):
        n = len(graph)
        width = 0
        for i in range(n):
            neighbors = set(graph[i])
            for j in range(i + 1, n):
                if j not in neighbors:
                    width += 1
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_graph(n)
        local_ind = local_indeterminacy(graph)
        circuit_width = circuit_monotone_width(graph)
        ratio = local_ind / circuit_width if circuit_width != 0 else float('inf')
        
        results.append({
            "metric_name": "Local Indeterminacy / Circuit Monotone Width Ratio",
            "metric_value": ratio,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": abs(ratio - 1) <= 0.1,
            "counterexample": f"Ratio {ratio} not within 10% of 1" if abs(ratio - 1) > 0.1 else ""
        })
    
    return {
        "metric_name": "Local Indeterminacy / Circuit Monotone Width Ratio",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(result["n_max"] for result in results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": next((result["counterexample"] for result in results if result["counterexample"]), "")
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio outside 10% of 1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")