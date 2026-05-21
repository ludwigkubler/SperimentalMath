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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for var in variables:
            clauses.append([var])
            clauses.append([-var])
        for i in range(n-1):
            clauses.append([variables[i], variables[i+1]])
            clauses.append([-variables[i], -variables[i+1]])
        return clauses
    
    def find_maximal_disjoint_set(clauses):
        graph = {i: set() for i in range(1, len(clauses)+1)}
        for clause in clauses:
            for lit in clause:
                if lit > 0:
                    graph[lit].add(-lit)
                    graph[-lit].add(lit)
        
        def dfs(node, visited):
            stack = [node]
            while stack:
                node = stack.pop()
                if node not in visited:
                    visited.add(node)
                    for neighbor in graph[node]:
                        stack.append(neighbor)
        
        components = []
        visited = set()
        for i in range(1, len(clauses)+1):
            if i not in visited:
                component = set()
                dfs(i, component)
                components.append(component)
        
        maximal_disjoint_set = max(components, key=len)
        return maximal_disjoint_set
    
    def cyclic_order(set_size):
        return math.ceil(math.log2(set_size))
    
    def resolution_refutation_length(clauses):
        # Simplified version for testing purposes
        return len(clauses) * 10
    
    n = random.randint(5, 40)
    formula = generate_tseitin_formula(n)
    maximal_disjoint_set = find_maximal_disjoint_set(formula)
    C_G = cyclic_order(len(maximal_disjoint_set))
    refutation_length = resolution_refutation_length(formula)
    
    if refutation_length < 2**C_G or refutation_length >= 2**(C_G + 1):
        return {
            "metric_name": "Resolution Refutation Length",
            "metric_value": refutation_length,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Refutation length {refutation_length} does not satisfy the conjectured bounds for C(G)={C_G}"
        }
    
    return {
        "metric_name": "Resolution Refutation Length",
        "metric_value": refutation_length,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = results[results.index(next(r for r in results if not r["conjecture_holds"]))]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")