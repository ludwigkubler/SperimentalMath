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
    
    def generate_boolean_function(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables) if random.randint(0, 1) else -var for var in variables]
            clauses.append(clause)
        return variables, clauses
    
    def conflict_graph(variables, clauses):
        graph = {var: set() for var in variables}
        for clause in clauses:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    if clause[i] != -clause[j]:
                        graph[abs(clause[i])].add(abs(clause[j]))
                        graph[abs(clause[j])].add(abs(clause[i]))
        return graph
    
    def is_connected(graph):
        visited = {node: False for node in graph}
        stack = [next(iter(graph))]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                stack.extend([neighbor for neighbor in graph[node] if not visited[neighbor]])
        return all(visited.values())
    
    def find_generators(graph):
        if not is_connected(graph):
            return []
        
        generators = []
        for node in graph:
            if len(graph[node]) == 1:
                generators.append(node)
        return generators
    
    def entropy(variables, clauses):
        n = len(variables)
        m = len(clauses)
        p = Fraction(m, 2**n)
        h = -p * math.log(p, 2) - (1 - p) * math.log(1 - p, 2)
        return h
    
    def max_coset_size(generators):
        if not generators:
            return 0
        size = 1
        for generator in generators:
            size *= len(graph[generator])
        return size
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            variables, clauses = generate_boolean_function(n, random.randint(1, n))
            graph = conflict_graph(variables, clauses)
            generators = find_generators(graph)
            h = entropy(variables, clauses)
            coset_size = max_coset_size(generators)
            results.append((n, len(generators), math.log(coset_size, 2), h))
    
    if not results:
        return {
            "metric_name": "Entropy",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(n for _, _, _, _ in results)
    instances_tested = len(results)
    conjecture_holds = all(math.prod(generators) * math.log(coset_size, 2) >= h + 1e-6 for _, generators, coset_size, h in results)
    
    return {
        "metric_name": "Entropy",
        "metric_value": sum(h for _, _, _, h in results) / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")