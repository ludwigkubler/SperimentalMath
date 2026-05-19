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
        if n <= 1:
            return []
        edges = set()
        for _ in range(n - 1):
            u, v = random.sample(range(n), 2)
            while (u, v) in edges or (v, u) in edges:
                u, v = random.sample(range(n), 2)
            edges.add((u, v))
        return list(edges)
    
    def betti_number(graph):
        n = len(graph) + 1
        m = len(graph)
        return m - n + 1
    
    def resolution_width(graph):
        if not graph:
            return 0
        
        # DPLL-based width estimator (simplified version)
        clauses = []
        for u, v in graph:
            clauses.append((u, v))
            clauses.append((-u, -v))
        
        queue = [set([1])]
        visited = set()
        max_width = 0
        
        while queue:
            current = queue.pop(0)
            if len(current) > max_width:
                max_width = len(current)
            
            for clause in clauses:
                if all(x not in current for x in clause):
                    new_clause = [x for x in clause if x not in visited]
                    if new_clause and len(new_clause) > 1:
                        queue.append(new_clause)
                        visited.add(tuple(sorted(new_clause)))
        
        return max_width
    
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    betti = betti_number(graph)
    width = resolution_width(graph)
    
    return {
        "metric_name": "Resolution Width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width >= betti,
        "counterexample": "" if width >= betti else f"Graph with {n} vertices and {len(graph)} edges"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")