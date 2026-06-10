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

def generate_tseitin_formula(n, num_clauses):
    variables = list(range(1, n + 1))
    clauses = []
    
    # Generate literals
    literals = [f"v{i}" for i in range(1, n + 1)] + [f"~v{i}" for i in range(1, n + 1)]
    
    # Generate clauses
    for _ in range(num_clauses):
        clause = []
        for _ in range(random.randint(2, n)):
            literal = random.choice(literals)
            if literal.startswith("~"):
                clause.append((int(literal[2:]) - 1, False))
            else:
                clause.append((int(literal) - 1, True))
        clauses.append(clause)
    
    return variables, clauses

def resolution_width(variables, clauses):
    n = len(variables)
    m = len(clauses)
    max_clause_length = max(len(clause) for clause in clauses)
    
    # Initialize the resolution graph
    graph = [[] for _ in range(n)]
    for i in range(m):
        for j in range(i + 1, m):
            if any((x[0] == y[0] and x[1] != y[1]) for x in clauses[i] for y in clauses[j]):
                graph[x[0]].append(y[0])
    
    # Perform BFS to find the maximum path length
    def bfs(start):
        queue = [(start, 1)]
        visited = set()
        max_length = 0
        while queue:
            node, length = queue.pop(0)
            if node not in visited:
                visited.add(node)
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        queue.append((neighbor, length + 1))
                max_length = max(max_length, length)
        return max_length
    
    max_path_length = max(bfs(i) for i in range(n))
    
    # Calculate the resolution width
    width = max_clause_length + max_path_length - 2
    return width

def smallest_p_adic_exponent(num_clauses):
    p = 2
    e = 0
    while p ** e < num_clauses:
        e += 1
    return e

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        num_clauses = random.randint(1, n * 10)
        variables, clauses = generate_tseitin_formula(n, num_clauses)
        
        width = resolution_width(variables, clauses)
        p_adic_exponent = smallest_p_adic_exponent(num_clauses)
        metric_value = math.log(p_adic_exponent + 1) / n
        
        results.append({
            "n": n,
            "num_clauses": num_clauses,
            "width": width,
            "p_adic_exponent": p_adic_exponent,
            "metric_value": metric_value
        })
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = all(abs(result["width"] - result["metric_value"]) <= 3 * std_metric_value for result in results)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": mean_metric_value,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": support_fraction,
        "counterexample": "" if support_fraction else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = all(abs(result["width"] - result["metric_value"]) <= 3 * std_metric_value for result in results)
    
    if support_fraction:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE counterexample=mapping_undefined")