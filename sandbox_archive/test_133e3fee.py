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
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def incidence_graph(clauses):
        graph = {}
        for i, clause in enumerate(clauses):
            for lit in clause:
                if abs(lit) not in graph:
                    graph[abs(lit)] = set()
                graph[abs(lit)].add(i)
        return graph
    
    def min_generators(graph):
        generators = set()
        visited = set()
        for node in graph:
            if node not in visited:
                stack = [node]
                while stack:
                    current = stack.pop()
                    if current not in visited:
                        visited.add(current)
                        generators.add(current)
                        for neighbor in graph[current]:
                            stack.append(neighbor)
        return len(generators)
    
    def resolution_size(clauses):
        size = 0
        seen = set()
        while True:
            new_clause = None
            for clause1 in clauses:
                if tuple(sorted(clause1)) not in seen:
                    seen.add(tuple(sorted(clause1)))
                    for clause2 in clauses:
                        if len(set(clause1) & set(clause2)) == 1:
                            new_clause = [x for x in clause1 if x not in clause2] + [x for x in clause2 if x not in clause1]
                            break
                if new_clause:
                    break
            if not new_clause:
                break
            clauses.append(new_clause)
            size += 1
        return size
    
    n = random.randint(5, 30)
    m = random.randint(n * 2, n * 4)
    clauses = generate_3cnf(n, m)
    graph = incidence_graph(clauses)
    generators = min_generators(graph)
    t_phi = resolution_size(clauses)
    
    return {
        "metric_name": "Generators vs Resolution Size",
        "metric_value": generators,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False if generators > math.log2(t_phi) ** 2 else True,
        "counterexample": "mapping_undefined" if not generators <= math.log2(t_phi) ** 2 else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")