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
    
    def generate_random_graph(n):
        graph = {i: set() for i in range(n)}
        edges = [(u, v) for u in range(n) for v in range(u + 1, n)]
        random.shuffle(edges)
        added_edges = 0
        while added_edges < n - 1:
            u, v = edges.pop()
            if u not in graph[v] and v not in graph[u]:
                graph[u].add(v)
                graph[v].add(u)
                added_edges += 1
        return graph
    
    def tseitin_formula(graph):
        literals = {i: f'x{i}' for i in range(len(graph))}
        clauses = []
        for u, v in graph.items():
            for w in v:
                clause = [f'-{literals[u]}', f'-{literals[v]}', f'{literals[w]}']
                clauses.append(clause)
                clause = [f'-{literals[u]}', f'{literals[v]}', f'-{literals[w]}']
                clauses.append(clause)
                clause = [f'{literals[u]}', f'-{literals[v]}', f'-{literals[w]}']
                clauses.append(clause)
        for i in range(len(graph)):
            clause = [f'-{literals[i]}'] + [f'{literals[j]}' for j in graph[i]]
            clauses.append(clause)
        return clauses
    
    def resolution_length(clauses):
        stack = []
        while True:
            new_clause = None
            for i in range(len(stack)):
                for j in range(i + 1, len(stack)):
                    if set(stack[i]) & set(stack[j]):
                        common_lit = list(set(stack[i]) & set(stack[j]))
                        new_clause = [lit for lit in stack[i] if lit != common_lit[0]] + \
                                     [lit for lit in stack[j] if lit != common_lit[1]]
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(stack)
            stack.append(new_clause)
    
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    formula = tseitin_formula(graph)
    length = resolution_length(formula)
    
    C = 1.0  # Constant C for the lower bound
    lower_bound = C * 2**(n/2) * math.log(n)
    
    return {
        "metric_name": "Resolution Length",
        "metric_value": length,
        "instances_tested": 1,
        "conjecture_holds": length >= lower_bound / 2 and length <= 2 * lower_bound,
        "counterexample": "" if length >= lower_bound / 2 and length <= 2 * lower_bound else f"Length {length} not within bounds"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")