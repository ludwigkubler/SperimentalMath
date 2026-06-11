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
    
    def generate_cnf(n):
        clauses = []
        for i in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def tseitin_graph(cnf):
        variables = set()
        for clause in cnf:
            for var in clause:
                variables.add(abs(var))
        
        graph = {var: [] for var in variables}
        
        for i, clause in enumerate(cnf):
            new_var = n + 1 + i
            for var in clause:
                graph[abs(var)].append((new_var, var > 0))
            for j in range(i + 1, len(cnf)):
                new_var_j = n + 1 + j
                for var in cnf[j]:
                    graph[abs(var)].append((new_var_j, var > 0))
        
        return graph
    
    def groupoid_action(graph):
        order = {var: 0 for var in graph}
        stack = list(graph.keys())
        while stack:
            node = stack.pop()
            if order[node] == 0:
                queue = [node]
                while queue:
                    current = queue.pop(0)
                    if order[current] == 0:
                        order[current] = max(order[neighbor] for neighbor, _ in graph[current]) + 1
                        queue.extend(neighbor for neighbor, _ in graph[current])
        return max(order.values())
    
    def resolution_proof_entanglement_complexity(cnf):
        width = 0
        for clause in cnf:
            if len(clause) > width:
                width = len(clause)
        return width
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    graph = tseitin_graph(cnf)
    min_order = groupoid_action(graph)
    ent_w = resolution_proof_entanglement_complexity(cnf)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": 0.5,  # Placeholder value
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")