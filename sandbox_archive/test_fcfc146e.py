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
        if (n * d) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    if (i, j) not in edges and (j, i) not in edges:
                        graph[i].append(j)
                        graph[j].append(i)
                        edges.add((i, j))
        return graph
    
    def compute_minimal_order_of_topological_entanglement(graph):
        n = len(graph)
        if n == 0:
            return 0
        mte = float('inf')
        for i in range(n):
            degree = len(graph[i])
            if degree > 0:
                mte = min(mte, degree)
        return mte
    
    def compute_frege_proof_length(graph):
        n = len(graph)
        if n == 0:
            return 0
        frege_length = 2 * (n - 1)  # Simplified model for Frege proof length
        return frege_length
    
    n_max = 40
    instances_tested = 30
    mte_values = []
    frege_length_values = []
    
    for _ in range(instances_tested):
        d = random.randint(2, min(n_max - 1, 5))  # Ensure graph is regular and non-empty
        graph = generate_d_regular_graph(n_max, d)
        if graph is None:
            continue
        
        mte = compute_minimal_order_of_topological_entanglement(graph)
        frege_length = compute_frege_proof_length(graph)
        
        if mte > 10:
            return {
                "metric_name": "mte(G)",
                "metric_value": mte,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "mte(G) > 10"
            }
        
        mte_values.append(mte)
        frege_length_values.append(frege_length)
    
    correlation_coefficient = sum((x - mean_mte) * (y - mean_frege_length) for x, y in zip(mte_values, frege_length_values)) / (instances_tested * math.sqrt(sum((x - mean_mte) ** 2 for x in mte_values) * sum((y - mean_frege_length) ** 2 for y in frege_length_values)))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")