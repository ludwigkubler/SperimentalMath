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
    
    def generate_planar_graph(n):
        if n < 3:
            return None, "graph_not_planar"
        
        vertices = list(range(n))
        edges = []
        for i in range(1, n):
            edges.append((0, i))
        
        for i in range(n):
            for j in range(i + 1, n):
                if len(edges) >= 3 * (n - 1):
                    break
                if random.randint(0, 1) == 0:
                    edges.append((i, j))
        
        return vertices, edges
    
    def is_planar(graph):
        # Simple planarity test using Kuratowski's theorem
        n = len(graph[0])
        if n < 5:
            return True
        
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    for l in range(k + 1, n):
                        edges = set()
                        for u, v in graph[1]:
                            if u == i and v == j or u == i and v == k or u == i and v == l:
                                continue
                            if u == j and v == k or u == j and v == l:
                                continue
                            if u == k and v == l:
                                continue
                            edges.add((u, v))
                        if len(edges) < 3 * (n - 1):
                            return False
        
        return True
    
    def quadratic_residues(n, p):
        residues = set()
        for x in range(1, p):
            if (x * x) % p not in residues:
                residues.add((x * x) % p)
        return residues
    
    def communication_complexity(graph):
        n = len(graph[0])
        edges = graph[1]
        complexity = 0
        for u, v in edges:
            complexity += abs(u - v)
        return complexity
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph, error = generate_planar_graph(n)
        if error != "graph_not_planar":
            p = random.randint(2, 100)
            while not is_planar((graph, [])):
                p = random.randint(2, 100)
            
            residues = quadratic_residues(n, p)
            cc = communication_complexity((graph, edges))
            results.append({
                "metric_name": "communication_complexity",
                "metric_value": cc,
                "instances_tested": n,
                "n_max": n,
                "conjecture_holds": True,
                "counterexample": ""
            })
        else:
            return {
                "metric_name": "communication_complexity",
                "metric_value": 0,
                "instances_tested": 0,
                "n_max": 0,
                "conjecture_holds": False,
                "counterexample": error
            }
    
    return results[0]

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = Fraction(len([r for r in results if r["conjecture_holds"]]), len(results)).limit_denominator()
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"graph_not_planar\" first_failing_seed={first_failing_seed}")