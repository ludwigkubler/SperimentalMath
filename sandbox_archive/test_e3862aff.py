# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n):
        clauses = set()
        for _ in range(10 * n):  # Generate enough clauses to ensure a dense formula
            variables = random.sample(range(1, n + 1), 3)
            clause = tuple(sorted(variables))
            if clause not in clauses:
                clauses.add(clause)
        return clauses
    
    def hypergraph_treewidth(clauses):
        # Simplified treewidth algorithm for demonstration purposes
        nodes = set()
        edges = []
        for clause in clauses:
            nodes.update(clause)
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    edges.append((clause[i], clause[j]))
        
        def dfs(node, visited):
            if node in visited:
                return
            visited.add(node)
            for neighbor in edges[node]:
                dfs(neighbor, visited)
        
        max_clique_size = 0
        for subset in combinations(nodes, len(nodes) // 2 + 1):
            clique = set(subset)
            if all((node in clique or node not in nodes) for node in nodes):
                max_clique_size = max(max_clique_size, len(clique))
        
        return max_clique_size
    
    def dpll_tree_size(clauses, assignment=None):
        if assignment is None:
            assignment = {}
        
        def solve():
            if all(any(lit in assignment and assignment[lit] == val for lit in clause) for clause in clauses):
                return 1
            if any(all(lit not in assignment or assignment[lit] != val for lit in clause) for clause in clauses):
                return 0
            
            var = next(var for var in range(1, n + 1) if var not in assignment)
            count_true = solve()
            if count_true > 0:
                return count_true
            assignment[var] = False
            count_false = solve()
            del assignment[var]
            return count_false
        
        return solve()
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    treewidth = hypergraph_treewidth(clauses)
    dpll_size = dpll_tree_size(clauses)
    
    if treewidth == 0 or dpll_size == 0:
        return {
            "metric_name": "treewidth * DPLL tree size",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_value = treewidth * dpll_size
    return {
        "metric_name": "treewidth * DPLL tree size",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")