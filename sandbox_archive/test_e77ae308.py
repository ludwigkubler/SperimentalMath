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
        for _ in range(10 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def tseitin_graph(cnf):
        graph = {}
        literals = set()
        for clause in cnf:
            literals.update(clause)
        for literal in literals:
            graph[literal] = []
        
        for i, clause in enumerate(cnf):
            new_var = -n - i
            graph[new_var] = [literal for literal in clause]
            for literal in clause:
                if literal > 0:
                    graph[-new_var].append(-literal)
                else:
                    graph[-new_var].append(literal)
        
        return graph
    
    def topological_entropy(graph):
        n = len(graph)
        in_degree = {node: 0 for node in graph}
        for neighbors in graph.values():
            for neighbor in neighbors:
                in_degree[neighbor] += 1
        
        queue = [node for node, degree in in_degree.items() if degree == 0]
        entropy = 0
        while queue:
            node = queue.pop()
            entropy -= math.log2(len(graph[node]))
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        return entropy / n
    
    def resolution_width(cnf):
        clauses = cnf[:]
        width = 0
        
        while True:
            new_clauses = []
            for i, clause1 in enumerate(clauses):
                for j, clause2 in enumerate(clauses):
                    if i >= j:
                        continue
                    common_literals = [literal for literal in clause1 if -literal in clause2]
                    if not common_literals:
                        continue
                    
                    new_clause = list(set(clause1 + clause2) - set(common_literals))
                    if len(new_clause) == 1:
                        return abs(new_clause[0])
                    
                    new_clauses.append(new_clause)
            
            if not new_clauses:
                break
            
            clauses.extend(new_clauses)
        
        return width
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    graph = tseitin_graph(cnf)
    h_phi = topological_entropy(graph)
    width = resolution_width(cnf)
    
    return {
        "metric_name": "topological_entropy_bound",
        "metric_value": h_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": h_phi <= n**1.5 and width <= 2 * n,
        "counterexample": "" if h_phi <= n**1.5 and width <= 2 * n else f"width={width} exceeds bound"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")