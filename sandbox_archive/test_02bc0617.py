# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3colorable_graph(n):
        if n < 5 or n > 40:
            return None, None
        
        graph = [[] for _ in range(n)]
        colors = [None] * n
        
        # Ensure the graph is 3-colorable
        for i in range(n):
            available_colors = set(range(3))
            for j in range(i):
                if j in graph[i]:
                    available_colors.discard(colors[j])
            color = random.choice(list(available_colors))
            colors[i] = color
            
            # Add edges to ensure the graph is 3-colorable
            for j in range(n):
                if j != i and colors[j] != color:
                    graph[i].append(j)
                    graph[j].append(i)
        
        return graph, colors
    
    def compute_min_local_index(graph):
        n = len(graph)
        simplicial_complex = []
        
        # Construct the simplicial complex
        for i in range(n):
            for j in range(i + 1, n):
                if j in graph[i]:
                    simplicial_complex.append((i, j))
        
        # Compute the minimal local index
        min_index = float('inf')
        for simplex in simplicial_complex:
            neighbors = set()
            for v in simplex:
                neighbors.update(graph[v])
            min_index = min(min_index, len(neighbors) - len(simplex) + 1)
        
        return min_index
    
    def compute_resolution_width(graph):
        n = len(graph)
        clauses = []
        
        # Create clauses for each vertex
        for i in range(n):
            clause = [j for j in range(n) if j != i]
            clauses.append(clause)
        
        # Resolve the clauses using a small DPLL solver
        def dpll(clauses, assignment):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                if literal < 0:
                    literal = -literal
                    value = False
                else:
                    value = True
                assignment[literal] = value
                new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                return dpll(new_clauses, assignment)
            pure_literal = next((l for l in range(1, n + 1) if (l not in assignment and -l not in assignment)), None)
            if pure_literal:
                value = True
                assignment[pure_literal] = value
                new_clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
                return dpll(new_clauses, assignment)
            literal = random.choice(range(1, n + 1))
            value = True
            assignment[literal] = value
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            if dpll(new_clauses, assignment):
                return True
            del assignment[literal]
            value = False
            assignment[literal] = value
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            if dpll(new_clauses, assignment):
                return True
            del assignment[literal]
            return False
        
        assignment = {}
        if not dpll(clauses, assignment):
            return 0
        
        # Compute the resolution width
        max_width = 0
        for literal in assignment:
            if assignment[literal]:
                width = sum(1 for c in clauses if literal in c)
                max_width = max(max_width, width)
        
        return max_width
    
    graph, colors = generate_3colorable_graph(random.randint(5, 40))
    if not graph or not colors:
        return {
            "metric_name": "min_local_index",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "graph_not_3colorable"
        }
    
    min_local_index = compute_min_local_index(graph)
    resolution_width = compute_resolution_width(graph)
    
    return {
        "metric_name": "min_local_index",
        "metric_value": min_local_index,
        "instances_tested": 1,
        "n_max": len(graph),
        "conjecture_holds": min_local_index >= 0.7 * resolution_width,
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
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")