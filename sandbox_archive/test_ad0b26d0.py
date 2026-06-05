# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n, d):
        if n % d != 0:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d and (i, j) not in edges and (j, i) not in edges:
                    graph[i].append(j)
                    graph[j].append(i)
                    edges.add((i, j))
        return graph
    
    def compute_local_induction_dimension(graph):
        n = len(graph)
        if n == 0:
            return 0
        max_dim = 0
        for i in range(n):
            neighbors = set(graph[i])
            dim = 1
            while True:
                new_neighbors = set()
                for neighbor in neighbors:
                    new_neighbors.update(set(graph[neighbor]) - {i})
                if len(new_neighbors) == 0:
                    break
                neighbors = new_neighbors
                dim += 1
            max_dim = max(max_dim, dim)
        return max_dim
    
    def compute_clause_subset_entropy(clauses):
        n = len(clauses)
        total = 2 ** n
        entropy = 0
        for i in range(1, 1 << n):
            subset = [j for j in range(n) if (i >> j) & 1]
            count = sum(all(j in clauses[k] for k in subset) for k in range(len(clauses)))
            prob = count / total
            if prob > 0:
                entropy += -prob * math.log2(prob)
        return entropy
    
    def generate_random_clauses(n, m):
        clauses = []
        for _ in range(m):
            clause = random.sample(range(n), random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        if graph is None:
            continue
        clauses = generate_random_clauses(n, int(2 * n))
        ltd = compute_local_induction_dimension(graph)
        entropy = compute_clause_subset_entropy(clauses)
        results.append({"n": n, "ltd": ltd, "entropy": entropy})
    
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max([r["n"] for r in results]),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    correlation = 0
    n_sum = sum(r["n"] for r in results)
    ltd_sum = sum(r["ltd"] for r in results)
    entropy_sum = sum(r["entropy"] for r in results)
    n_ltd_product_sum = sum(r["n"] * r["ltd"] for r in results)
    n_entropy_product_sum = sum(r["n"] * r["entropy"] for r in results)
    
    correlation_numerator = n_ltd_product_sum * len(results) - n_sum * ltd_sum
    correlation_denominator = math.sqrt((n_sum ** 2 - sum(r["n"] ** 2 for r in results)) * (ltd_sum ** 2 - sum(r["ltd"] ** 2 for r in results)))
    
    if correlation_denominator == 0:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max([r["n"] for r in results]),
            "conjecture_holds": False,
            "counterexample": "zero_denominator"
        }
    
    correlation = correlation_numerator / correlation_denominator
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max([r["n"] for r in results]),
        "conjecture_holds": correlation >= 0.5,
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
        std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")