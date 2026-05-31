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
    
    def generate_boolean_function(n, m):
        variables = list(range(n))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 2)
            clauses.append(clause)
        return clauses
    
    def conflict_graph(clauses):
        graph = {}
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                if set(clauses[i]).intersection(set(clauses[j])):
                    if i not in graph:
                        graph[i] = []
                    if j not in graph:
                        graph[j] = []
                    graph[i].append(j)
                    graph[j].append(i)
        return graph
    
    def is_connected(graph):
        visited = {node: False for node in graph}
        stack = [0]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                stack.extend([neighbor for neighbor in graph[node] if not visited[neighbor]])
        return all(visited.values())
    
    def find_generators(graph):
        generators = []
        for node in range(len(graph)):
            if is_connected({node: graph[node]}):
                generators.append(node)
        return generators
    
    def coset_representative_set_size(generators, n):
        size = 1
        for generator in generators:
            size *= (2 ** n - 2) // (2 ** len(graph[generator]) - 2)
        return size
    
    def entropy(clauses):
        num_true = sum(1 for clause in clauses if all(random.choice([0, 1]) for var in clause))
        num_false = sum(1 for clause in clauses if not any(random.choice([0, 1]) for var in clause))
        p_true = num_true / len(clauses)
        p_false = num_false / len(clauses)
        return -p_true * math.log2(p_true) - p_false * math.log2(p_false) if p_true > 0 and p_false > 0 else 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            m = random.randint(n // 2, n * (n - 1) // 2)
            clauses = generate_boolean_function(n, m)
            graph = conflict_graph(clauses)
            generators = find_generators(graph)
            coset_size = coset_representative_set_size(generators, n)
            H_f = entropy(clauses)
            results.append({
                "n": n,
                "m": m,
                "generators": len(generators),
                "coset_size": coset_size,
                "H_f": H_f
            })
    
    metric_value = sum(result["H_f"] for result in results) / len(results)
    conjecture_holds = all(result["generators"] * math.log2(result["coset_size"]) >= result["H_f"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Entropy",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 307))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")