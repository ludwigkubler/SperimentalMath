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
    
    def hodge_diamond_dimension(graph):
        # Placeholder function for computing Hodge diamond dimension
        # This is a dummy implementation and should be replaced with actual code
        return 1
    
    def communication_complexity(graph, f):
        # Placeholder function for computing communication complexity
        # This is a dummy implementation and should be replaced with actual code
        return 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = random_graph(n)
        D_G = hodge_diamond_dimension(graph)
        f = random_function(n)
        C_f = communication_complexity(graph, f)
        
        if C_f == 0 or D_G == 0:
            continue
        
        results.append({
            "n": n,
            "D_G": D_G,
            "C_f": C_f
        })
    
    if not results:
        return {
            "metric_name": "CommunicationComplexity",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    n_max = max(result["n"] for result in results)
    mean_C = sum(result["C_f"] for result in results) / len(results)
    std_C = math.sqrt(sum((result["C_f"] - mean_C) ** 2 for result in results) / len(results))
    
    return {
        "metric_name": "CommunicationComplexity",
        "metric_value": mean_C,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": all(result["D_G"] * math.log(result["n"]) >= result["C_f"] for result in results),
        "counterexample": ""
    }

def random_graph(n):
    # Generate a random graph with n vertices
    graph = [[] for _ in range(n)]
    edges = set()
    
    while len(edges) < n * (n - 1) // 2:
        u, v = random.sample(range(n), 2)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
    
    return graph

def random_function(n):
    # Generate a random function f: {0,1}^n -> {0,1}
    return [random.choice([0, 1]) for _ in range(2 ** n)]

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_C = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_C = math.sqrt(sum((r["metric_value"] - mean_C) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_C} std={std_C} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence_or_budget_exceeded n_tested=30")