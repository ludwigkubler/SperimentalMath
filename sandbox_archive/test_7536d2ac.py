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
    
    def generate_d_regular_graph(n, d):
        if (d * n) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        for i in range(n):
            neighbors = random.sample(range(n), d - len(graph[i]))
            for neighbor in neighbors:
                if (i, neighbor) not in edges and (neighbor, i) not in edges:
                    graph[i].append(neighbor)
                    graph[neighbor].append(i)
                    edges.add((i, neighbor))
        return graph
    
    def cheeger_constant(graph):
        n = len(graph)
        min_cut = float('inf')
        for node in range(n):
            neighbors = graph[node]
            cut_size = len(neighbors)
            boundary_size = sum(1 for neighbor in neighbors if len(graph[neighbor]) > d)
            if boundary_size < min_cut:
                min_cut = boundary_size
        return min_cut / n
    
    def resolution_length(graph):
        # Simplified DPLL-based algorithm with pruning
        stack = []
        assignment = {}
        clauses = []
        for node in range(len(graph)):
            clause = [node, -node]
            clauses.append(clause)
        
        def dpll():
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                assignment[literal] = True
                clauses = [c for c in clauses if literal not in c and -literal not in c]
            pure_literal = next((l for l in range(1, len(graph) + 1) if (l not in assignment and -l not in assignment)), None)
            if pure_literal:
                assignment[pure_literal] = True
                clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
            if not clauses:
                return True
            literal = random.choice([l for l in range(1, len(graph) + 1) if l not in assignment and -l not in assignment])
            assignment[literal] = True
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            if dpll():
                return True
            del assignment[literal]
            assignment[-literal] = True
            new_clauses.extend([c for c in clauses if literal in c or -literal in c])
            if dpll():
                return True
            del assignment[-literal]
            return False
        
        length = 0
        while not dpll():
            length += 1
        return length
    
    n = random.randint(5, 40)
    d = 2 * random.randint(1, n // 2)
    graph = generate_d_regular_graph(n, d)
    if graph is None:
        return {
            "metric_name": "Resolution Length",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    h_G = cheeger_constant(graph)
    length = resolution_length(graph)
    
    return {
        "metric_name": "Resolution Length",
        "metric_value": length,
        "instances_tested": 1,
        "conjecture_holds": length >= 2 ** (h_G * math.log(2)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")