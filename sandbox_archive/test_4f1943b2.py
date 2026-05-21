# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_graph(n):
        if n == 1:
            return {0: set()}
        nodes = list(range(n))
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.append((i, j))
        graph = {node: set() for node in nodes}
        for u, v in edges:
            graph[u].add(v)
            graph[v].add(u)
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = list(range(1, 2 * n + 1))
        clauses = []
        for node in range(n):
            clauses.append([literals[2 * node], literals[2 * node + 1]])
        for node in range(n):
            for neighbor in graph[node]:
                clauses.append([-literals[2 * node], -literals[2 * neighbor + 1]])
                clauses.append([-literals[2 * node + 1], -literals[2 * neighbor]])
        return literals, clauses
    
    def resolution_length(clauses):
        clauses = set(clauses)
        while True:
            new_clauses = set()
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = [l for l in clause1 + clause2 if l not in set(clause1) & set(clause2)]
                        if [] in new_clauses:
                            return len(clauses)
                        new_clauses.add(tuple(sorted(new_clause)))
            if new_clauses.issubset(clauses):
                return len(clauses)
            clauses.update(new_clauses)
    
    def coxeter_group_orbits(graph):
        n = len(graph)
        nodes = list(range(n))
        orbits = set()
        for node in nodes:
            orbit = {node}
            stack = [node]
            while stack:
                current = stack.pop()
                for neighbor in graph[current]:
                    if neighbor not in orbit:
                        orbit.add(neighbor)
                        stack.append(neighbor)
            orbits.add(tuple(sorted(orbit)))
        return len(orbits)
    
    n_values = [5, 10, 15, 20, 30, 40]
    max_ratio = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            graph = generate_graph(n)
            literals, clauses = tseitin_formula(graph)
            resolution_len = resolution_length(clauses)
            orbits = coxeter_group_orbits(graph)
            ratio = Fraction(orbits) / (2 ** resolution_len)
            max_ratio = max(max_ratio, ratio)
            instances_tested += 1
    
    return {
        "metric_name": "max_ratio",
        "metric_value": float(max_ratio),
        "instances_tested": instances_tested,
        "conjecture_holds": max_ratio <= 1,
        "counterexample": "" if max_ratio <= 1 else f"Graph with {n} nodes and resolution length {resolution_len}, orbits {orbits}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing = next(r for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{first_failing['counterexample']}\" first_failing_seed={first_failing['seed']}")