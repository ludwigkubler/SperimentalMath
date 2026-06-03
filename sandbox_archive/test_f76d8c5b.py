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
        if n < 2:
            return None
        graph = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            graph[i][i] = 0
        return graph
    
    def compute_geometric_entropy(graph):
        if not graph:
            return 0.0
        n = len(graph)
        adjacency_matrix = [sum(row) for row in graph]
        total_edges = sum(adjacency_matrix) / 2
        entropy = 0.0
        for degree in adjacency_matrix:
            if degree > 0:
                p = degree / (2 * total_edges)
                entropy += -p * math.log(p, 2)
        return entropy
    
    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            row_sum = sum(graph[i])
            if row_sum > 0:
                rank += 1
        return rank
    
    def solve_lits(lits_true, lits_false):
        # Placeholder for a simple SAT solver (not used here)
        return True
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        graph = generate_graph(n)
        if not graph:
            continue
        
        entropy = compute_geometric_entropy(graph)
        rank = communication_complexity_rank(graph)
        
        if rank == 0:
            continue
        
        metric_values.append(entropy / rank)
    
    mean_value = sum(metric_values) / len(metric_values) if metric_values else 0
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    
    conjecture_holds = all(x <= 1.5 for x in metric_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "H(G)/r(k)",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 50, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}**}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["n_max"] >= 16 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")