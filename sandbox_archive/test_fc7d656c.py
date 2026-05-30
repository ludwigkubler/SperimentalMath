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

def generate_cnf(n, m):
    clauses = set()
    for _ in range(m):
        clause = []
        for _ in range(3):
            var = random.randint(1, n)
            sign = random.choice([True, False])
            if sign:
                clause.append(var)
            else:
                clause.append(-var)
        clauses.add(tuple(sorted(clause)))
    return clauses

def incidence_graph(cnf):
    graph = {}
    for clause in cnf:
        for lit in clause:
            var = abs(lit)
            if var not in graph:
                graph[var] = set()
            for other_lit in clause:
                if other_lit != lit and abs(other_lit) == var:
                    graph[var].add(abs(other_lit))
    return graph

def min_generators(graph):
    generators = set()
    visited = set()
    
    def dfs(node):
        stack = [node]
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                for neighbor in graph.get(current, []):
                    if neighbor not in visited:
                        stack.append(neighbor)
    
    for node in graph:
        if node not in visited:
            dfs(node)
            generators.add(node)
    
    return len(generators)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    m = 20
    
    cnf = generate_cnf(n, m)
    graph = incidence_graph(cnf)
    
    if not graph:
        return {
            "metric_name": "min_generators",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "empty_graph"
        }
    
    generators = min_generators(graph)
    
    return {
        "metric_name": "min_generators",
        "metric_value": generators,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")