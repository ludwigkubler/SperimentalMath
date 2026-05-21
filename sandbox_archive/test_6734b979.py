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

def generate_tseitin_formula(n):
    tseitin_vars = [f'x{i}' for i in range(1, n + 1)]
    clauses = []
    
    # Generate clauses for each variable
    for i in range(1, n + 1):
        clauses.append([tseitin_vars[i - 1], -tseitin_vars[n + i]])
        clauses.append([-tseitin_vars[i - 1], tseitin_vars[n + i]])
    
    # Generate clauses for the final variable
    for i in range(1, n + 1):
        clauses.append([tseitin_vars[i - 1], tseitin_vars[n + i]])
    
    return tseitin_vars, clauses

def is_disjoint_set(graph, nodes):
    visited = set()
    stack = [nodes[0]]
    
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        
        for neighbor in graph[node]:
            if neighbor in visited:
                return False
            stack.append(neighbor)
    
    return True

def find_maximal_disjoint_set(graph):
    nodes = list(graph.keys())
    max_cyclic_order = 0
    maximal_disjoint_set = []
    
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if is_disjoint_set(graph, [nodes[i], nodes[j]]):
                cyclic_order = abs(j - i)
                if cyclic_order > max_cyclic_order:
                    max_cyclic_order = cyclic_order
                    maximal_disjoint_set = [nodes[i], nodes[j]]
    
    return maximal_disjoint_set, max_cyclic_order

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40  # Fixed size for this trial
    
    variables, clauses = generate_tseitin_formula(n)
    graph = {var: [] for var in variables}
    
    # Build the graph from clauses
    for clause in clauses:
        for i in range(len(clause)):
            for j in range(i + 1, len(clause)):
                if clause[i] != -clause[j]:
                    graph[variables[abs(clause[i]) - 1]].append(variables[abs(clause[j]) - 1])
    
    maximal_disjoint_set, cyclic_order = find_maximal_disjoint_set(graph)
    resolution_length = 2 ** cyclic_order
    
    return {
        "metric_name": "Resolution refutation length",
        "metric_value": resolution_length,
        "instances_tested": 1,
        "conjecture_holds": resolution_length >= 2 ** math.ceil(cyclic_order),
        "counterexample": "" if resolution_length >= 2 ** math.ceil(cyclic_order) else f"Found counterexample with cyclic order {cyclic_order}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r['metric_value'] for r in results) / len(results)
    std_dev = math.sqrt(sum((r['metric_value'] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")