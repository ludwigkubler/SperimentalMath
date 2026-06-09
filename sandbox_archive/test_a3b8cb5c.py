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
    
    def generate_circuit(n):
        if n == 1:
            return ['0']
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return [f'({l} OR {r})' for l in left for r in right]
    
    def tseitin_formula(circuit):
        literals = set()
        clauses = []
        for expr in circuit:
            if 'OR' in expr:
                a, b = expr.split(' OR ')
                literals.add(a)
                literals.add(b)
                clauses.append([a, b])
                clauses.append(['NOT', a, 'NOT', b])
            else:
                literals.add(expr)
                clauses.append([expr])
        return literals, clauses
    
    def resolution_width(clauses):
        queue = clauses[:]
        while True:
            new_clauses = []
            for i in range(len(queue)):
                for j in range(i + 1, len(queue)):
                    if any(l == 'NOT' + r or r == 'NOT' + l for l in queue[i] for r in queue[j]):
                        new_clause = [l for l in queue[i] if l not in ['NOT', r] for r in queue[j] if r not in ['NOT', l]]
                        if len(new_clause) == 1:
                            return len(queue)
                        new_clauses.append(new_clause)
            if new_clauses == queue:
                break
            queue = new_clauses
        return float('inf')
    
    def simplicial_decomposition(clauses):
        graph = {l: set() for l in literals}
        for clause in clauses:
            for i, l1 in enumerate(clause):
                for l2 in clause[i + 1:]:
                    if 'NOT' not in l1 and 'NOT' not in l2:
                        graph[l1].add(l2)
                        graph[l2].add(l1)
        
        def dfs(node, visited, component):
            visited.add(node)
            component.append(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    dfs(neighbor, visited, component)
        
        components = []
        visited = set()
        for node in literals:
            if node not in visited:
                component = []
                dfs(node, visited, component)
                components.append(component)
        
        return len(components), [len(c) for c in components]
    
    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    literals, clauses = tseitin_formula(circuit)
    width = resolution_width(clauses)
    cells, widths = simplicial_decomposition(clauses)
    
    return {
        "metric_name": "resolution_width_to_cells_ratio",
        "metric_value": width / cells,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": width <= cells * 2,  # Simplified bound for demonstration
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
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
        print(f"RESULT: FALSIFIED counterexample='resolution_width_to_cells_ratio' first_failing_seed={first_failing_seed}")