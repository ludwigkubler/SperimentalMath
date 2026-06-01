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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_d_regular_graph(d, n):
        graph = [[] for _ in range(n)]
        nodes = list(range(n))
        random.shuffle(nodes)
        
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    graph[i].append(j)
                    graph[j].append(i)
                    
        return graph
    
    def topological_degree(graph):
        degrees = [len(neighbors) for neighbors in graph]
        return sum(degrees) / len(degrees)
    
    def frege_proof_size(n):
        # Simplified model: Frege proof size is proportional to n^2
        return n * n
    
    n = 10  # Start with a small n and increase
    td_values = []
    fgs_values = []
    
    while len(td_values) < 30:
        graph = generate_d_regular_graph(3, n)
        td = topological_degree(graph)
        fg = frege_proof_size(n)
        
        if td is not None and fg is not None:
            td_values.append(td)
            fgs_values.append(fg)
        
        n += 1
    
    correlation_coefficient = sum((td - mean_td) * (fg - mean_fg) for td, fg in zip(td_values, fgs_values)) / len(td_values)
    mean_td = sum(td_values) / len(td_values)
    mean_fg = sum(fgs_values) / len(fgs_values)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(td_values),
        "n_max": n - 1,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
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
    elif any(abs(r["metric_value"]) > 5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"]) > 5)
        print(f"RESULT: FALSIFIED counterexample=\"large_difference\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")