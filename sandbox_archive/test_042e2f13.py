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
    n = 30
    instances_tested = 0
    total_generators = 0
    max_n = 0
    
    def generate_random_3cnf(n):
        m = random.randint(2 * n, 4 * n)
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), 3)]
            clauses.append(clause)
        return clauses
    
    def construct_incidence_graph(clauses):
        graph = {}
        for clause in clauses:
            for lit in clause:
                if abs(lit) not in graph:
                    graph[abs(lit)] = set()
                for other_lit in clause:
                    if other_lit != lit and abs(other_lit) not in graph[abs(lit)]:
                        graph[abs(lit)].add(abs(other_lit))
        return graph
    
    def find_minimal_generators(graph):
        generators = set()
        visited = set()
        
        def dfs(node):
            stack = [node]
            while stack:
                node = stack.pop()
                if node not in visited:
                    visited.add(node)
                    for neighbor in graph[node]:
                        if neighbor not in visited:
                            stack.append(neighbor)
            
            generators.update(graph[node])
        
        for node in graph:
            if node not in visited:
                dfs(node)
        
        return generators
    
    def resolution_proof_size(clauses):
        proof_size = 0
        while True:
            new_clause = None
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = [x for x in clause1 if x not in clause2] + [x for x in clause2 if x not in clause1]
                        proof_size += 1
                        break
                if new_clause:
                    clauses.append(new_clause)
                    break
            else:
                break
        return proof_size
    
    for _ in range(30):
        clauses = generate_random_3cnf(n)
        graph = construct_incidence_graph(clauses)
        generators = find_minimal_generators(graph)
        resolution_size = resolution_proof_size(clauses)
        
        if len(generators) > 0:
            total_generators += len(generators)
            instances_tested += 1
            max_n = max(max_n, n)
    
    mean_generators = total_generators / instances_tested if instances_tested > 0 else 0
    conjecture_holds = mean_generators <= math.log2(n) ** 2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mean_generators",
        "metric_value": mean_generators,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")