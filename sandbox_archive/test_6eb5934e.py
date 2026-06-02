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
    
    def generate_d_regular_graph(n, d):
        if (d * n) % 2 != 0:
            return None
        graph = [[] for _ in range(n)]
        degree = [0] * n
        edges_added = 0
        
        while edges_added < d * n // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and v not in graph[u]:
                graph[u].append(v)
                graph[v].append(u)
                degree[u] += 1
                degree[v] += 1
                edges_added += 1
        
        return graph
    
    def tseitin_formula(graph, n):
        clauses = []
        literals = {}
        
        for i in range(n):
            literals[i] = f'x{i}'
            literals[-i] = f'-x{i}'
        
        for i in range(n):
            clause = [literals[i]]
            for j in graph[i]:
                if degree[j] % 2 == 1:
                    clause.append(literals[j])
                else:
                    clause.append(f'-{literals[j]}')
            clauses.append(clause)
        
        return clauses
    
    def hodge_dimension(n):
        # Constructive mapping to compute Hodge dimension
        # This is a placeholder implementation for demonstration purposes
        return n // 2
    
    def entropy(clauses):
        counts = {}
        for clause in clauses:
            count = len(set(clause))
            if count not in counts:
                counts[count] = 0
            counts[count] += 1
        
        total_clauses = sum(counts.values())
        h = 0.0
        for count, freq in counts.items():
            p = freq / total_clauses
            h -= p * math.log2(p)
        
        return h
    
    n_values = [10, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        if graph is None:
            continue
        
        clauses = tseitin_formula(graph, n)
        hd = hodge_dimension(n)
        H = entropy(clauses)
        
        results.append({
            "n": n,
            "hd(G)": hd,
            "H(φ_G)": H
        })
    
    if not results:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = sum((r["hd(G)"] - n_values[0] / 2) * (r["H(φ_G)"] - n_values[0]) for r in results) / len(results)
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": 0.5 <= correlation <= 1.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")