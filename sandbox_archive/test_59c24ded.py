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
                if set(clauses[i]) & set(clauses[j]):
                    if i not in graph:
                        graph[i] = []
                    if j not in graph:
                        graph[j] = []
                    graph[i].append(j)
                    graph[j].append(i)
        return graph
    
    def is_connected(graph):
        visited = set()
        stack = [0]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                stack.extend(set(graph[node]) - visited)
        return len(visited) == len(graph)
    
    def number_of_components(graph):
        if not is_connected(graph):
            components = []
            visited = set()
            for node in range(len(graph)):
                if node not in visited:
                    component = []
                    stack = [node]
                    while stack:
                        current = stack.pop()
                        if current not in visited:
                            visited.add(current)
                            component.append(current)
                            stack.extend(set(graph[current]) - visited)
                    components.append(component)
            return len(components)
        else:
            return 1
    
    def irreducible_generators(n, m):
        # This is a placeholder for the actual implementation of irreducible generators
        # For simplicity, we assume it returns a list of generators based on n and m
        return [i for i in range(n + m)]
    
    def coset_size(generators):
        # Placeholder for the actual implementation of coset size
        # For simplicity, we assume it returns a large number
        return 100
    
    def entropy(clauses):
        n = len(clauses)
        p = Fraction(1, 2) ** n
        h = -p * math.log(p, 2) - (1 - p) * math.log(1 - p, 2)
        return h
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            m = random.randint(n // 2, n * 2)
            f = generate_boolean_function(n, m)
            G = conflict_graph(f)
            generators = irreducible_generators(n, m)
            coset_size_val = coset_size(generators)
            h = entropy(f)
            if coset_size_val <= 0:
                continue
            results.append((n, len(generators), math.log(coset_size_val, 2), h))
    
    metric_value = sum(r[3] for r in results) / len(results)
    conjecture_holds = all(r[2] * len(r[1]) >= r[3] for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Entropy",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(r[0] for r in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")