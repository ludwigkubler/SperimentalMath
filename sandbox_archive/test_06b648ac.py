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
    
    def generate_3_colorable_graph(n):
        graph = [[0] * n for _ in range(n)]
        colors = [-1] * n
        color_set = [0, 1, 2]
        
        def is_valid(color, node):
            for i in range(n):
                if graph[node][i] and colors[i] == color:
                    return False
            return True
        
        def backtrack(node):
            if node == n:
                return True
            for c in color_set:
                if is_valid(c, node):
                    colors[node] = c
                    if backtrack(node + 1):
                        return True
                    colors[node] = -1
            return False
        
        if not backtrack(0):
            raise ValueError("Failed to generate a valid 3-colorable graph")
        
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    graph[i][j] = graph[j][i] = 1
        
        return graph
    
    def simplicial_complex(graph):
        n = len(graph)
        simplices = []
        
        def add_face(face):
            face.sort()
            simplices.append(tuple(face))
        
        for i in range(n):
            add_face([i])
        
        for u in range(n):
            for v in range(u + 1, n):
                if graph[u][v]:
                    add_face([u, v])
        
        return simplices
    
    def min_local_index(simplices):
        n = len(simplices)
        local_indices = [0] * n
        
        for face in simplices:
            for i in range(len(face)):
                neighbors = set()
                for j in range(len(face)):
                    if i != j and (face[i], face[j]) in simplices:
                        neighbors.add(j)
                local_indices[face[i]] += len(neighbors)
        
        return max(local_indices)
    
    def resolution_width(graph):
        n = len(graph)
        clauses = []
        
        for u in range(n):
            clause = [i + 1 if graph[u][i] else -(i + 1) for i in range(n)]
            clauses.append(clause)
        
        stack = []
        assignment = {}
        
        def dpll():
            while True:
                unit_clause = next((c for c in clauses if len(c) == 1), None)
                if unit_clause:
                    literal = unit_clause[0]
                    if literal > 0:
                        assignment[literal] = True
                    else:
                        assignment[-literal] = False
                    stack.append(literal)
                    clauses = [c for c in clauses if literal not in c and -literal not in c]
                elif len(clauses) == 0:
                    return True
                else:
                    literal = next((i + 1 for i in range(n) if i + 1 not in assignment and -(i + 1) not in assignment), None)
                    stack.append(literal)
                    assignment[literal] = True
        
        dpll()
        
        width = max(len([l for l in stack if assignment[l]]) for _ in range(10))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_3_colorable_graph(n)
        simplices = simplicial_complex(graph)
        min_index = min_local_index(simplices)
        width = resolution_width(graph)
        results.append((min_index, width))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    min_indices, widths = zip(*results)
    correlation_coefficient = sum((x - mean_min) * (y - mean_width) for x, y in zip(min_indices, widths)) / len(results)
    mean_min = sum(min_indices) / len(min_indices)
    mean_width = sum(widths) / len(widths)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "correlation_coefficient < 0.7"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")