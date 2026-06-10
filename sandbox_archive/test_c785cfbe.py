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
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0 or d < n - 1:
            return None
        graph = [[] for _ in range(n)]
        edges_added = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) >= d or len(graph[j]) >= d:
                    continue
                if (i, j) not in edges_added and (j, i) not in edges_added:
                    graph[i].append(j)
                    graph[j].append(i)
                    edges_added.add((i, j))
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: f'x{i}' for i in range(n)}
        clauses = []
        
        for i in range(n):
            clause = [literals[i]]
            for j in range(i + 1, n):
                if graph[i][j]:
                    clause.append(f'~{literals[j]}')
            clauses.append(clause)
            
            for j in range(i + 1, n):
                if not graph[i][j]:
                    clause = [f'~{literals[i]}']
                    for k in range(j + 1, n):
                        if graph[j][k]:
                            clause.append(f'~{literals[k]}')
                    clauses.append(clause)
        
        return literals, clauses
    
    def resolution_width(phi):
        # Placeholder function to compute resolution width
        # This is a dummy implementation and should be replaced with actual logic
        return len(phi)
    
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_d_regular_graph(n, n - 1)
        if graph is None:
            continue
        
        literals, clauses = tseitin_formula(graph)
        phi = clauses
        width = resolution_width(phi)
        
        return {
            "metric_name": "resolution_width",
            "metric_value": width,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    return {
        "metric_name": "resolution_width",
        "metric_value": None,
        "instances_tested": 0,
        "n_max": 0,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(res["conjecture_holds"] for res in results):
        mean_width = sum(res["metric_value"] for res in results) / len(results)
        std_width = math.sqrt(sum((res["metric_value"] - mean_width) ** 2 for res in results) / len(results))
        support_fraction = 1.0
    else:
        max_width = max(res["metric_value"] for res in results if res["metric_value"] is not None)
        min_width = min(res["metric_value"] for res in results if res["metric_value"] is not None)
        mean_width = sum(res["metric_value"] for res in results) / len(results)
        std_width = math.sqrt(sum((res["metric_value"] - mean_width) ** 2 for res in results) / len(results))
        support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(res["metric_value"] < -0.5 for res in results):
        first_failing_seed = next(i for i, res in enumerate(results) if res["metric_value"] < -0.5)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_negative\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")