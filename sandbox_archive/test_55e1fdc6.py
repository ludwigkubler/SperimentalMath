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
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def dpll_solve(clauses):
        # Simplified DPLL solver
        assignment = [False] * len(variables)
        stack = []
        
        def solve():
            if not clauses:
                return True
            literal = find_unassigned_literal(clauses)
            if literal is None:
                return False
            
            for value in [True, False]:
                assignment[literal[0]] = value
                new_clauses = propagate(literal, clauses)
                if solve():
                    return True
                backtrack()
        
        def find_unassigned_literal(clauses):
            for clause in clauses:
                for literal in clause:
                    var = abs(literal) - 1
                    if assignment[var] == False:
                        return (var + 1, literal > 0)
            return None
        
        def propagate(literal, clauses):
            new_clauses = []
            for clause in clauses:
                if literal[0] not in [abs(lit) for lit in clause]:
                    new_clause = [lit for lit in clause if abs(lit) != literal[0]]
                    if not new_clause:
                        return None
                    new_clauses.append(new_clause)
            return new_clauses
        
        def backtrack():
            assignment[literal[0] - 1] = False
        
        solve()
        return assignment
    
    n = random.randint(5, 40)
    graph_edges = generate_graph(n)
    
    # Tseitin encoding
    variables = [f"v{i+1}" for i in range(n)]
    clauses = []
    for i in range(n):
        clauses.append([f"v{i+1}"])
        clauses.append([-f"v{i+1}"])
    
    for (u, v) in graph_edges:
        clauses.append([f"v{u+1}", f"v{v+1}", -f"e_{u+1}_{v+1}"])
        clauses.append([f"v{u+1}", -f"v{v+1}", f"e_{u+1}_{v+1}"])
        clauses.append([-f"v{u+1}", f"v{v+1}", f"e_{u+1}_{v+1}"])
        clauses.append([-f"v{u+1}", -f"v{v+1}", -f"e_{u+1}_{v+1}"])
    
    for i in range(n):
        for j in range(i + 1, n):
            clauses.append([f"e_{i+1}_{j+1}", f"e_{j+1}_{i+1}"])
            clauses.append([-f"e_{i+1}_{j+1}", -f"e_{j+1}_{i+1}"])
    
    proof_size = len(dpll_solve(clauses))
    
    # Euler characteristic for a graph with n vertices and m edges
    m = len(graph_edges)
    euler_characteristic = n - m
    
    return {
        "metric_name": "Euler characteristic",
        "metric_value": abs(euler_characteristic),
        "instances_tested": 1,
        "conjecture_holds": abs(euler_characteristic) / math.log(n) > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")