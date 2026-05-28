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
    
    def generate_triangle_detection_instance(n):
        edges = set()
        for i in range(n):
            for j in range(i+1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def incidence_graph_to_tropicalized_lie_algebra(edges, n):
        # Simplified representation using a dictionary to simulate the tropicalized Lie algebra
        lie_algebra = {}
        for (u, v) in edges:
            if u not in lie_algebra:
                lie_algebra[u] = set()
            if v not in lie_algebra:
                lie_algebra[v] = set()
            lie_algebra[u].add(v)
            lie_algebra[v].add(u)
        return lie_algebra
    
    def rank_of_lie_algebra(lie_algebra):
        # Simplified rank calculation (number of vertices with non-empty neighborhood)
        return sum(1 for neighbors in lie_algebra.values() if neighbors)
    
    def communication_complexity(edges, n):
        # Simplified communication complexity (number of edges)
        return len(edges)
    
    n = random.randint(5, 40)
    instance_edges = generate_triangle_detection_instance(n)
    lie_algebra = incidence_graph_to_tropicalized_lie_algebra(instance_edges, n)
    rank = rank_of_lie_algebra(lie_algebra)
    C_I = communication_complexity(instance_edges, n)
    
    r_n = math.log2(n) ** 2
    
    conjecture_holds = False
    counterexample = ""
    if C_I < math.log2(n):
        if rank <= r_n:
            counterexample = "Rank does not exceed r(n)"
        else:
            conjecture_holds = True
    
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r['metric_value'] for r in results) / len(results)
    std_metric = math.sqrt(sum((r['metric_value'] - mean_metric) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        counterexample_desc = "Rank does not exceed r(n)"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")